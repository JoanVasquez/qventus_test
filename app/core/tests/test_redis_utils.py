import json
from unittest import TestCase
from unittest.mock import patch
from core.utils import redis as redis_utils


# 🧪 Test class for Redis utility functions
class RedisUtilsTests(TestCase):
    # ⚙️ Setup test data and keys
    def setUp(self):
        self.key = "test_key"
        self.model_name = "Part"
        self.version_key = f"version:{self.model_name.lower()}"
        self.sample_data = {"message": "hello"}

    # 💾 Test setting cache data
    @patch.object(redis_utils, "redis_client")
    def test_set_cache(self, mock_redis):
        redis_utils.set_cache(self.key, self.sample_data)
        mock_redis.set.assert_called_with(self.key, json.dumps(self.sample_data), ex=60)

    # 📖 Test retrieving cache data successfully
    @patch.object(redis_utils, "redis_client")
    def test_get_cache_returns_data(self, mock_redis):
        mock_redis.get.return_value = json.dumps(self.sample_data)
        result = redis_utils.get_cache(self.key)
        self.assertEqual(result, self.sample_data)

    # 🚫 Test retrieving non-existent cache data
    @patch.object(redis_utils, "redis_client")
    def test_get_cache_returns_none(self, mock_redis):
        mock_redis.get.return_value = None
        result = redis_utils.get_cache(self.key)
        self.assertIsNone(result)

    # 🗑️ Test deleting cache data
    @patch.object(redis_utils, "redis_client")
    def test_delete_cache(self, mock_redis):
        redis_utils.delete_cache(self.key)
        mock_redis.delete.assert_called_with(self.key)

    # 📊 Test getting existing model version
    @patch.object(redis_utils, "redis_client")
    def test_get_model_version_returns_existing(self, mock_redis):
        mock_redis.get.return_value = "3"
        version = redis_utils.get_model_version(self.model_name)
        self.assertEqual(version, 3)

    # 🆕 Test initializing new model version
    @patch.object(redis_utils, "redis_client")
    def test_get_model_version_initializes(self, mock_redis):
        mock_redis.get.return_value = None
        version = redis_utils.get_model_version(self.model_name)
        mock_redis.set.assert_called_with(self.version_key, 1)
        self.assertEqual(version, 1)

    # ⬆️ Test incrementing model version
    @patch.object(redis_utils, "redis_client")
    def test_bump_model_version(self, mock_redis):
        redis_utils.bump_model_version(self.model_name)
        mock_redis.incr.assert_called_with(self.version_key)
