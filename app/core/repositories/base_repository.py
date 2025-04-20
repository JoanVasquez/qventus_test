# 🔄 Import required Django and custom exceptions
from django.core.exceptions import ObjectDoesNotExist
from ..utils.logger import get_logger
from ..exceptions.custom_exceptions import (
    EntityNotFoundException,
    EntityCreateException,
    EntityUpdateException,
    EntityDeleteException,
    EntityFetchAllException,
    EntityFetchException,
)


# 📦 Base repository class for common CRUD operations
class BaseRepository:
    # 🏗️ Initialize repository with model class
    def __init__(self, model_class):
        self.model = model_class
        self.logger = get_logger(f"{model_class.__name__}Repository")

    # ➕ Create new entity
    def create(self, data: dict):
        try:
            instance = self.model.objects.create(**data)
            # ✅ Log success
            self.logger.info(
                "🟢 Entity created successfully",
                extra={"data": data}
            )
            return instance
        except Exception as e:
            # ❌ Log failure
            self.logger.error(
                "❌ Failed to create entity",
                extra={"data": data, "error": str(e)}
            )
            raise EntityCreateException()

    # 📝 Update existing entity
    def update(self, instance, data: dict):
        try:
            for attr, value in data.items():
                setattr(instance, attr, value)
            instance.save()
            # ✅ Log success
            self.logger.info(
                "🟢 Entity updated successfully",
                extra={
                    "id": instance.id,
                    "updated_data": data,
                },
            )
            return instance
        except Exception as e:
            # ❌ Log failure
            self.logger.error(
                "❌ Failed to update entity",
                extra={"id": instance.id, "error": str(e)}
            )
            raise EntityUpdateException()

    # 🔍 Find entity by ID
    def find_by_id(self, pk):
        try:
            instance = self.model.objects.get(pk=pk)
            # ✅ Log success
            self.logger.info("🟢 Entity retrieved", extra={"id": pk})
            return instance
        except ObjectDoesNotExist:
            # ⚠️ Not found
            self.logger.warning("⚠️ Entity not found", extra={"id": pk})
            raise EntityNotFoundException()
        except Exception as e:
            # ❌ Log failure
            self.logger.error(
                "❌ Error retrieving entity",
                extra={"id": pk, "error": str(e)}
            )
            raise EntityFetchException()

    # 📋 Get all entities
    def find_all(self):
        try:
            instances = self.model.objects.all()
            # ✅ Log success
            self.logger.info("🟢 All entities retrieved successfully")
            return instances
        except Exception as e:
            # ❌ Log failure
            self.logger.error(
                "❌ Failed to retrieve all entities",
                extra={"error": str(e)},
            )
            raise EntityFetchAllException()

    # 🗑️ Delete entity
    def delete(self, instance):
        try:
            instance.delete()
            # ✅ Log success
            self.logger.info(
                "🟢 Entity deleted successfully",
                extra={"id": instance.id}
            )
            return True
        except Exception as e:
            # ❌ Log failure
            self.logger.error(
                "❌ Failed to delete entity",
                extra={"id": instance.id, "error": str(e)},
            )
            raise EntityDeleteException()
