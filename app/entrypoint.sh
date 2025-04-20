#!/bin/bash

# 🔄 Wait for database to be ready
python manage.py wait_for_db

# 📦 Run database migrations
python manage.py migrate

# 🚀 Start Django development server
exec python manage.py runserver 0.0.0.0:8000
