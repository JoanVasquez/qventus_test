test:
	docker compose run -e DJANGO_ENV=test web python manage.py test --settings=settings.base
