# 🔧 Serializer for Part model
# Handles conversion between Part model instances and JSON/dict data
from rest_framework import serializers
from core.models import Part


class PartSerializer(serializers.ModelSerializer):
    """
    📝 Serializer class for the Part model
    Inherits from ModelSerializer to automatically create fields based on model
    """
    class Meta:
        # 🎯 Configure serializer metadata
        model = Part  # Model to serialize
        fields = '__all__'  # Include all model fields in serialization
