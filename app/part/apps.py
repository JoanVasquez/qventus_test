# 🔧 Django App Configuration for Part Module
from django.apps import AppConfig


class PartConfig(AppConfig):
    # 🔑 Specifies the primary key type for models
    default_auto_field = 'django.db.models.BigAutoField'
    # 📝 The name of the Django app
    name = 'part'
