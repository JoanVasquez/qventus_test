# 📦 Django model for managing parts/components
from django.db import models


class Part(models.Model):
    # 📝 Basic part information
    name = models.CharField(max_length=150)  # Part name/title
    sku = models.CharField(max_length=30)    # Stock keeping unit identifier
    description = models.TextField(
        max_length=1024
    )  # Detailed part description

    # ⚖️ Physical properties
    weight_ounces = models.PositiveIntegerField()  # Weight in ounces

    # 🔄 Status
    is_active = models.BooleanField(default=True)
    # Whether part is active/available

    def __str__(self):
        # 🔤 String representation of part
        return f"{self.name} ({self.sku})"

    class Meta:
        # 🗃️ Database configuration
        db_table = "part"
