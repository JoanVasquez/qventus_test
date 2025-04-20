from django.test import TestCase
from rest_framework.exceptions import APIException
from rest_framework import status

from core.exceptions.custom_exceptions import (
    EntityNotFoundException,
    EntityCreateException,
    EntityUpdateException,
    EntityDeleteException,
    EntityFetchAllException,
    EntityFetchException,
)


# 🧪 Test class for custom exceptions
class CustomExceptionsTest(TestCase):

    # 🔍 Helper method to validate exception attributes
    def assert_exception_attrs(
        self, exc_class, expected_status, expected_detail, expected_code
    ):
        exc = exc_class()
        self.assertIsInstance(exc, APIException)
        self.assertEqual(exc.status_code, expected_status)
        self.assertEqual(exc.default_detail, expected_detail)
        self.assertEqual(exc.default_code, expected_code)

    # ❌ Test for entity not found exception
    def test_entity_not_found_exception(self):
        self.assert_exception_attrs(
            EntityNotFoundException,
            status.HTTP_404_NOT_FOUND,
            "Entity not found.",
            "not_found"
        )

    # ➕ Test for entity creation exception
    def test_entity_create_exception(self):
        self.assert_exception_attrs(
            EntityCreateException,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Failed to create entity.",
            "create_failed"
        )

    # 🔄 Test for entity update exception
    def test_entity_update_exception(self):
        self.assert_exception_attrs(
            EntityUpdateException,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Failed to update entity.",
            "update_failed"
        )

    # 🗑️ Test for entity deletion exception
    def test_entity_delete_exception(self):
        self.assert_exception_attrs(
            EntityDeleteException,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Failed to delete entity.",
            "delete_failed"
        )

    # 📋 Test for fetching all entities exception
    def test_entity_fetch_all_exception(self):
        self.assert_exception_attrs(
            EntityFetchAllException,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Failed to retrieve all entities.",
            "fetch_all_failed"
        )

    # 🔎 Test for fetching single entity exception
    def test_entity_fetch_exception(self):
        self.assert_exception_attrs(
            EntityFetchException,
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Failed to retrieve entity.",
            "fetch_failed"
        )
