# 🔧 Import required modules
import os
from django.core.wsgi import get_wsgi_application

# ⚙️ Set default Django settings module path
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.base')

# 🚀 Initialize WSGI application
application = get_wsgi_application()
