# 🔄 Redis cache utilities
from ..utils.redis import (
    set_cache,          # 💾 Store data in cache
    get_cache,          # 📖 Retrieve data from cache
    get_model_version,  # 🏷️ Get current model version
    bump_model_version,  # ⬆️ Increment model version
)

# 📝 Django model utilities
# 🔄 Convert model instance to dictionary
from django.forms.models import model_to_dict

# ⚠️ Custom exception classes
from ..exceptions.custom_exceptions import (
    EntityNotFoundException,   # 🔍 When entity not found
    EntityCreateException,    # ❌ When create fails
    EntityUpdateException,    # 🔄 When update fails
    EntityDeleteException,    # 🗑️ When delete fails
    EntityFetchAllException,  # 📋 When fetching all fails
    EntityFetchException,    # 🎯 When fetching one fails
)


# 🏗️ Base service class that handles common CRUD operations with caching
class BaseService:
    # 🎯 Initialize service with repository and caching config
    def __init__(self, repository, model_name: str, ttl_config=None):
        self.repository = repository  # 📦 Data access layer
        self.model_name = model_name.lower()  # 📝 Model name for cache keys
        self.ttl_config = ttl_config or {
            "all": 60,
            "by_id": 60,
        }  # ⏱️ Cache TTL settings

    # 🔑 Generate cache key with version
    def _key(self, suffix: str):
        version = get_model_version(self.model_name)
        return f"{self.model_name}:v{version}:{suffix}"

    # 🔍 Find single entity by ID
    def find_by_id(self, pk):
        key = self._key(str(pk))
        try:
            # 📖 Check cache first
            cached = get_cache(key)
            if cached:
                return cached

            # 🔍 Get from repository if not in cache
            instance = self.repository.find_by_id(pk)
            if not instance:
                raise EntityNotFoundException()

            # 💾 Cache the result
            result = model_to_dict(instance)
            set_cache(key, result, ttl=self.ttl_config.get("by_id", 60))
            return result
        except EntityNotFoundException:
            raise
        except Exception as e:
            raise EntityFetchException(detail=str(e))

    # 📋 Get all entities
    def find_all(self):
        key = self._key("all")
        try:
            # 📖 Check cache first
            cached = get_cache(key)
            if cached:
                return cached

            # 📋 Get all from repository
            queryset = self.repository.find_all()
            result = [model_to_dict(obj) for obj in queryset]
            # 💾 Cache the results
            set_cache(key, result, ttl=self.ttl_config.get("all", 60))
            return result
        except Exception as e:
            raise EntityFetchAllException(detail=str(e))

    # ➕ Create new entity
    def create(self, data):
        try:
            instance = self.repository.create(data)
            bump_model_version(self.model_name)  # 🔄 Invalidate cache
            return instance
        except Exception as e:
            raise EntityCreateException(detail=str(e))

    # 🔄 Update existing entity
    def update(self, instance, data):
        try:
            updated = self.repository.update(instance, data)
            bump_model_version(self.model_name)  # 🔄 Invalidate cache
            return updated
        except Exception as e:
            raise EntityUpdateException(detail=str(e))

    # 🗑️ Delete entity
    def delete(self, instance):
        try:
            result = self.repository.delete(instance)
            bump_model_version(self.model_name)  # 🔄 Invalidate cache
            return result
        except Exception as e:
            raise EntityDeleteException(detail=str(e))
