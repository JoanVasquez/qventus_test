# 🔄 Import required system modules
import os
import sys


# 🚀 Main function that initializes and runs Django
def main():
    # 🛠️ Set default Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.base')
    try:
        # ⚙️ Import Django's command line executor
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # ❌ Handle case where Django is not installed
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? "
        ) from exc
    # ▶️ Execute Django commands
    execute_from_command_line(sys.argv)


# 🎯 Script entry point
if __name__ == '__main__':
    main()
