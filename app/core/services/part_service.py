# 🔧 Import required base classes and repositories
from .base_service import BaseService
from ..repositories.part_repository import PartRepository
from ..exceptions.custom_exceptions import (
    EntityFetchException,  # ❌ Exception for entity fetch failures
)


# 🏭 Service class for handling Part-related operations
class PartService(BaseService):
    def __init__(self):
        # ⚙️ Configure cache TTL settings:
        # - 'all' parts cache expires in 120 seconds
        # - Individual part 'by_id' cache expires in 300 seconds
        ttl_config = {"all": 120, "by_id": 300}  # ⏱️ Cache expiration times
        super().__init__(
            PartRepository(), "part", ttl_config=ttl_config
        )  # 🔄 Initialize base service

    def find_most_common_words_in_descriptions(self, top_n=5):
        """
        🔍 Returns the top N most common words across all part descriptions.

        Parameters:
        - top_n (int): 📊 Number of most common words to return (default: 5)

        Returns:
        - list: 📝 List of tuples containing (word, frequency)

        Raises:
        - EntityFetchException: ❌ If there's an error fetching the data
        """
        try:
            # 🔎 Fetch the most common words using the repository method
            common_words = self.repository.most_common_words_in_descriptions(
                top_n
            )
            return common_words  # ✅ Return successful result
        except Exception as e:
            raise EntityFetchException(
                detail=str(e)
            )  # 🚫 Handle and re-raise errors
