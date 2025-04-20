# 🔧 Django App Configuration
from django.apps import AppConfig


# 📦 Core Application Configuration Class
class CoreConfig(AppConfig):
    # 🔑 Default primary key field type
    default_auto_field = 'django.db.models.BigAutoField'
    # 📝 Application name identifier
    name = 'core'
