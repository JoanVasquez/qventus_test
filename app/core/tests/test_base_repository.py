# 🔧 Imports for testing and functionality
from django.test import TestCase
from core.repositories.base_repository import BaseRepository
from core.models import Part
from unittest.mock import patch
from core.exceptions.custom_exceptions import (
    EntityNotFoundException,
    EntityCreateException,
    EntityUpdateException,
    EntityDeleteException,
    EntityFetchAllException,
    EntityFetchException,
)


# 📝 Helper function to generate test part data
def get_part_data(overrides=None):
    data = {
        "name": "Test Part",
        "sku": "SKU123",
        "description": "Sample part description",
        "weight_ounces": 10,
        "is_active": True
    }
    if overrides:
        data.update(overrides)
    return data


# 🧪 Test cases for BaseRepository
class BaseRepositoryTests(TestCase):
    # ⚙️ Setup test environment
    def setUp(self):
        self.repo = BaseRepository(Part)

    # ✅ Test successful creation of a part
    def test_create_success(self):
        data = get_part_data()
        instance = self.repo.create(data)
        self.assertIsNotNone(instance.id)
        self.assertEqual(instance.name, data["name"])

    # ❌ Test creation failure handling
    def test_create_failure_raises_exception(self):
        with patch.object(Part.objects, 'create', side_effect=Exception("DB error")):
            with self.assertRaises(EntityCreateException):
                self.repo.create(get_part_data({"name": "fail"}))

    # 🔄 Test successful update of a part
    def test_update_success(self):
        instance = Part.objects.create(**get_part_data({"name": "old"}))
        updated = self.repo.update(instance, {"name": "new"})
        self.assertEqual(updated.name, "new")

    # ⚠️ Test update failure handling
    def test_update_failure_raises_exception(self):
        instance = Part.objects.create(**get_part_data({"name": "update"}))
        with patch.object(instance, 'save', side_effect=Exception("DB error")):
            with self.assertRaises(EntityUpdateException):
                self.repo.update(instance, {"name": "error"})

    # 🔍 Test successful find by ID
    def test_find_by_id_success(self):
        instance = Part.objects.create(**get_part_data())
        found = self.repo.find_by_id(instance.id)
        self.assertEqual(found.id, instance.id)

    # 🚫 Test not found scenario
    def test_find_by_id_not_found(self):
        with self.assertRaises(EntityNotFoundException):
            self.repo.find_by_id(999)

    # 💥 Test general exception handling for find by ID
    def test_find_by_id_general_exception(self):
        with patch.object(Part.objects, 'get', side_effect=Exception("DB error")):
            with self.assertRaises(EntityFetchException):
                self.repo.find_by_id(1)

    # 📋 Test successful retrieval of all parts
    def test_find_all_success(self):
        Part.objects.create(**get_part_data({"name": "a"}))
        Part.objects.create(**get_part_data({"name": "b", "sku": "SKU124"}))
        all_items = self.repo.find_all()
        self.assertEqual(len(all_items), 2)

    # 🚨 Test failure handling for find all
    def test_find_all_failure(self):
        with patch.object(Part.objects, 'all', side_effect=Exception("DB error")):
            with self.assertRaises(EntityFetchAllException):
                self.repo.find_all()

    # 🗑️ Test successful deletion
    def test_delete_success(self):
        instance = Part.objects.create(**get_part_data({"name": "del"}))
        result = self.repo.delete(instance)
        self.assertTrue(result)
        self.assertEqual(Part.objects.count(), 0)

    # ⛔ Test delete failure handling
    def test_delete_failure(self):
        instance = Part.objects.create(**get_part_data({"name": "fail"}))
        with patch.object(instance, 'delete', side_effect=Exception("DB error")):
            with self.assertRaises(EntityDeleteException):
                self.repo.delete(instance)
