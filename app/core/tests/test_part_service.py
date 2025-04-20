# 🧪 Test suite for the PartService class
from django.test import TestCase
from unittest.mock import patch
from core.services.part_service import PartService
from core.exceptions.custom_exceptions import EntityFetchException


class PartServiceTests(TestCase):
    # 🏗️ Setup method to initialize test environment
    def setUp(self):
        self.service = PartService()

    # 📊 Test successful retrieval of most common words
    @patch("core.services.part_service.PartRepository")
    def test_find_most_common_words_success(self, MockRepo):
        # 🎯 Arrange: Set up mock repository with test data
        mock_repo_instance = MockRepo.return_value
        mock_repo_instance.most_common_words_in_descriptions.return_value = [
            ("widget", 5),  # 🔝 Most frequent word
            ("gear", 3),    # 🥈 Second most frequent
            ("bolt", 2),    # 🥉 Third most frequent
        ]

        # 🛠️ Inject mock repository into service
        service = PartService()
        service.repository = mock_repo_instance

        # ✅ Act: Call the service method
        result = service.find_most_common_words_in_descriptions(3)

        # 🔍 Assert: Verify results and method calls
        self.assertEqual(result, [("widget", 5), ("gear", 3), ("bolt", 2)])
        mock_repo_instance.most_common_words_in_descriptions.assert_called_once_with(3)

    # ⚠️ Test error handling when database operation fails
    @patch("core.services.part_service.PartRepository")
    def test_find_most_common_words_raises_exception(self, MockRepo):
        # ❌ Arrange: Configure mock to simulate database error
        mock_repo_instance = MockRepo.return_value
        mock_repo_instance.most_common_words_in_descriptions.side_effect = \
            Exception("Database error")

        # 🛠️ Inject mock repository into service
        service = PartService()
        service.repository = mock_repo_instance

        # 🚫 Act + Assert: Verify exception handling
        with self.assertRaises(EntityFetchException) as ctx:
            service.find_most_common_words_in_descriptions(5)

        # ✋ Verify error message
        self.assertIn("Database error", str(ctx.exception))
