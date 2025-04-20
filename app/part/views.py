# 🔧 Imports for Django REST framework and Django core
from rest_framework.views import APIView
from rest_framework import status
from django.http import JsonResponse
from django.forms.models import model_to_dict

# 📦 Import services and utilities
from core.services.part_service import PartService
from .serializers import PartSerializer
from core.utils.response import success_response, error_response

# Initialize part service
part_service = PartService()


# 📝 View for handling list operations on Parts
class PartListView(APIView):
    # 📋 Get all parts
    def get(self, request):
        parts = part_service.find_all()
        return JsonResponse(
            success_response(parts, "Parts retrieved"),
            status=status.HTTP_200_OK
        )

    # ➕ Create new part
    def post(self, request):
        serializer = PartSerializer(data=request.data)
        if serializer.is_valid():
            part = part_service.create(serializer.validated_data)
            data = {"id": part.id}
            return JsonResponse(
                success_response(data, "Part created"),
                status=status.HTTP_201_CREATED
            )

        return JsonResponse(
            error_response(
                message="Validation failed.",
                code="validation_error",
                details=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            ),
            status=status.HTTP_400_BAD_REQUEST
        )


# 🔍 View for handling operations on individual Parts
class PartDetailView(APIView):
    # 👀 Get single part by ID
    def get(self, request, pk):
        part = part_service.find_by_id(pk)
        return JsonResponse(
            success_response(part, "Part retrieved"),
            status=status.HTTP_200_OK
        )

    # ✏️ Update existing part
    def put(self, request, pk):
        instance = part_service.repository.find_by_id(pk)
        if not instance:
            return JsonResponse(
                error_response(
                    "Part not found", code="not_found", status_code=404
                ),
                status=404
            )

        serializer = PartSerializer(instance, data=request.data)
        if serializer.is_valid():
            updated = part_service.update(
                instance, serializer.validated_data
            )
            return JsonResponse(
                success_response(model_to_dict(updated), "Part updated"),
                status=status.HTTP_200_OK
            )

        return JsonResponse(
            error_response(
                message="Validation failed.",
                code="validation_error",
                details=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            ),
            status=status.HTTP_400_BAD_REQUEST
        )

    # 🗑️ Delete part
    def delete(self, request, pk):
        instance = part_service.repository.find_by_id(pk)
        if not instance:
            return JsonResponse(
                error_response(
                    "Part not found", code="not_found", status_code=404
                ),
                status=404
            )

        part_service.delete(instance)
        return JsonResponse(
            success_response(message="Part deleted", code=204),
            status=status.HTTP_204_NO_CONTENT
        )


# 📊 View for retrieving statistics about Parts
class PartStatsView(APIView):
    # 📈 Get most common words in part descriptions
    def get(self, request):
        top_n = request.GET.get("top_n", 5)
        try:
            top_n = int(top_n)
        except ValueError:
            return JsonResponse(
                error_response(
                    message="Invalid value for top_n",
                    code="invalid_parameter",
                    status_code=status.HTTP_400_BAD_REQUEST
                ),
                status=status.HTTP_400_BAD_REQUEST
            )

        common_words = part_service.find_most_common_words_in_descriptions(
            top_n
        )
        return JsonResponse(
            success_response(common_words, "Most common words retrieved"),
            status=status.HTTP_200_OK
        )
