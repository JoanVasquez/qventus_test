# 🔌 --- Imports --- 🔌
import redis
import json
from django.conf import settings


# 🔄 --- Redis Client Singleton --- 🔄
class RedisClient:
    # Singleton instance
    _client = None

    @classmethod
    def get_client(cls):
        # Returns singleton Redis client instance
        # Creates new connection if none exists
        # Uses settings.REDIS_URL for connection
        if cls._client is None:
            cls._client = redis.Redis.from_url(
                settings.REDIS_URL, decode_responses=True
            )
        return cls._client


# 🌐 --- Global Instance --- 🌐
# Global Redis client instance for reuse
redis_client = RedisClient.get_client()


# 📦 --- Caching Utilities --- 📦
def get_cache(key: str):
    # 🔍 Retrieves cached value for given key
    # ⚠️ Returns None if key doesn't exist
    # 🔄 Automatically deserializes JSON data
    value = redis_client.get(key)
    return json.loads(value) if value else None


def set_cache(key: str, data, ttl: int = 60):
    # 💾 Stores data in cache with given key and TTL
    # ⏱️ Default TTL is 60 seconds
    # 🔄 Automatically serializes data to JSON
    redis_client.set(key, json.dumps(data), ex=ttl)


def delete_cache(key: str):
    # 🗑️ Removes key from cache
    # ⚡ Operation is idempotent
    redis_client.delete(key)


# 🏷️ --- Versioning for Tag-Based Invalidation --- 🏷️
def get_version_key(model_name: str):
    # 🔑 Generates Redis key for model version
    # 📝 Format: version:{lowercase_model_name}
    return f"version:{model_name.lower()}"


def get_model_version(model_name: str):
    # 📊 Gets current version number for model
    # 🆕 Initializes to 1 if not found
    # 🔢 Returns integer version number
    key = get_version_key(model_name)
    version = redis_client.get(key)
    if not version:
        redis_client.set(key, 1)
        return 1
    return int(version)


def bump_model_version(model_name: str):
    # ⬆️ Increments version number for model
    # 🔄 Atomic operation using Redis INCR
    redis_client.incr(get_version_key(model_name))
