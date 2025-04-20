from rest_framework.exceptions import APIException
from rest_framework import status


# ❌ Exception raised when an entity is not found
class EntityNotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Entity not found."
    default_code = "not_found"


# ❌ Exception raised when entity creation fails
class EntityCreateException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Failed to create entity."
    default_code = "create_failed"


# ❌ Exception raised when entity update fails
class EntityUpdateException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Failed to update entity."
    default_code = "update_failed"


# ❌ Exception raised when entity deletion fails
class EntityDeleteException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Failed to delete entity."
    default_code = "delete_failed"


# ❌ Exception raised when fetching all entities fails
class EntityFetchAllException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Failed to retrieve all entities."
    default_code = "fetch_all_failed"


# ❌ Exception raised when fetching a single entity fails
class EntityFetchException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Failed to retrieve entity."
    default_code = "fetch_failed"
