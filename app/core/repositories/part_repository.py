# 🏭 Repository for managing Part entities in the database
# Inherits from BaseRepository to provide CRUD operations
from .base_repository import BaseRepository
from ..models import Part
from collections import Counter  # 🔢 For counting word frequencies
import re  # 🔍 For text pattern matching


class PartRepository(BaseRepository):
    """
    📦 Part repository for managing part data.
    Handles database operations for Part objects including:
    - 📝 Creating new parts
    - 🔎 Retrieving parts
    - 🔄 Updating part information
    - 🗑️ Deleting parts
    """

    def __init__(self):
        # 🔄 Initialize repository with Part model
        super().__init__(Part)

    def most_common_words_in_descriptions(self, top_n=5):
        """
        🔍 Returns the top N most common words across all part descriptions.

        Args:
            top_n (int): 🔢 Number of most common words to return (default=5)

        Returns:
            list: 📊 List of tuples containing (word, frequency) pairs
        """
        # 📝 Get all descriptions from database
        descriptions = self.model.objects.values_list("description", flat=True)

        # 🔄 Combine and normalize text to lowercase
        all_text = " ".join(filter(None, descriptions)).lower()

        # ✂️ Tokenize text into individual words, ignoring punctuation
        words = re.findall(r'\b\w+\b', all_text)

        # 📊 Count frequencies and get top N most common words
        common_words = Counter(words).most_common(top_n)

        return common_words
