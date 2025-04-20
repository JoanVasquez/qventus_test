from django.test import TestCase
from unittest.mock import MagicMock, patch
from core.services.base_service import BaseService
from core.exceptions.custom_exceptions import (
    EntityCreateException,
    EntityUpdateException,
    EntityDeleteException,
    EntityFetchAllException,
    EntityFetchException,
)


# 🧪 Test suite for BaseService class
class BaseServiceTests(TestCase):
    # 🔧 Setup test environment
    def setUp(self):
        self.repo_mock = MagicMock()
        self.service = BaseService(self.repo_mock, "Part")

    # 🔍 Test finding entity by ID from cache
    @patch("core.services.base_service.get_cache", return_value={"id": 1})
    def test_find_by_id_from_cache(self, mock_cache):
        result = self.service.find_by_id(1)
        self.assertEqual(result["id"], 1)
        self.repo_mock.find_by_id.assert_not_called()

    # 🗄️ Test finding entity by ID from database
    @patch("core.services.base_service.get_cache", return_value=None)
    @patch("core.services.base_service.set_cache")
    @patch("core.services.base_service.model_to_dict", return_value={"id": 1})
    def test_find_by_id_from_db(self, mock_to_dict, mock_set, mock_get):
        mock_instance = MagicMock()
        self.repo_mock.find_by_id.return_value = mock_instance
        result = self.service.find_by_id(1)
        self.assertEqual(result["id"], 1)

    # ❌ Test failure scenario for find by ID
    def test_find_by_id_failure(self):
        self.repo_mock.find_by_id.side_effect = Exception("fail")
        with self.assertRaises(EntityFetchException):
            self.service.find_by_id(99)

    # 📋 Test successful retrieval of all entities
    @patch("core.services.base_service.get_cache", return_value=None)
    @patch("core.services.base_service.set_cache")
    @patch("core.services.base_service.model_to_dict", return_value={"id": 1})
    def test_find_all_success(self, mock_to_dict, mock_set, mock_get):
        self.repo_mock.find_all.return_value = [MagicMock()]
        result = self.service.find_all()
        self.assertEqual(result, [{"id": 1}])

    # ❌ Test failure scenario for find all
    def test_find_all_failure(self):
        self.repo_mock.find_all.side_effect = Exception("fail")
        with self.assertRaises(EntityFetchAllException):
            self.service.find_all()

    # ➕ Test successful entity creation
    def test_create_success(self):
        self.repo_mock.create.return_value = MagicMock()
        self.assertIsNotNone(self.service.create({"name": "test"}))

    # ❌ Test failure scenario for entity creation
    def test_create_failure(self):
        self.repo_mock.create.side_effect = Exception("fail")
        with self.assertRaises(EntityCreateException):
            self.service.create({"bad": "data"})

    # 📝 Test successful entity update
    def test_update_success(self):
        instance = MagicMock()
        self.repo_mock.update.return_value = instance
        result = self.service.update(instance, {"name": "updated"})
        self.assertEqual(result, instance)

    # ❌ Test failure scenario for entity update
    def test_update_failure(self):
        instance = MagicMock()
        self.repo_mock.update.side_effect = Exception("fail")
        with self.assertRaises(EntityUpdateException):
            self.service.update(instance, {"name": "fail"})

    # 🗑️ Test successful entity deletion
    def test_delete_success(self):
        instance = MagicMock()
        self.repo_mock.delete.return_value = True
        self.assertTrue(self.service.delete(instance))

    # ❌ Test failure scenario for entity deletion
    def test_delete_failure(self):
        instance = MagicMock()
        self.repo_mock.delete.side_effect = Exception("fail")
        with self.assertRaises(EntityDeleteException):
            self.service.delete(instance)
