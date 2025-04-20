from django.test import TestCase
from core.models import Part
from core.repositories.part_repository import PartRepository


# 🧪 Test class for Part Repository functionality
class PartRepositoryTests(TestCase):
    # 🔧 Set up test data
    def setUp(self):
        # Initialize repository
        self.repo = PartRepository()
        # Create first test part
        Part.objects.create(
            name="Part One",
            sku="SKU1",
            description="This is a sample description with common words.",
            weight_ounces=10,
            is_active=True,
        )
        # Create second test part
        Part.objects.create(
            name="Part Two",
            sku="SKU2",
            description="Common words repeat in this second test description.",
            weight_ounces=20,
            is_active=True,
        )

    # ✅ Test default behavior of most common words
    def test_most_common_words_default(self):
        # Should return the top 5 words by default
        result = self.repo.most_common_words_in_descriptions()
        # 🔍 Verify result is a non-empty list
        self.assertTrue(isinstance(result, list))
        self.assertGreater(len(result), 0)
        # 🔍 Verify each item is a tuple with 2 elements
        self.assertTrue(all(isinstance(word, tuple) and len(word) == 2 for word in result))

    # ✅ Test custom number of words returned
    def test_most_common_words_custom_top_n(self):
        # Should return the specified number of words
        top_n = 3
        result = self.repo.most_common_words_in_descriptions(top_n)
        # 🔍 Verify correct number of results returned
        self.assertEqual(len(result), top_n)

    # ✅ Test behavior with no data
    def test_most_common_words_empty_descriptions(self):
        # 🧪 Clear all parts and test empty case
        Part.objects.all().delete()
        result = self.repo.most_common_words_in_descriptions()
        # 🔍 Verify empty list is returned
        self.assertEqual(result, [])
