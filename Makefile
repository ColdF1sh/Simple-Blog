install:
	pip install -r requirements.txt

migrate:
	python manage.py makemigrations
	python manage.py migrate

run:
	python manage.py runserver

test:
	python manage.py test

lint:
	python -m flake8 .

quality:
	python -m pylint accounts blog_project posts

createsuperuser:
	python manage.py createsuperuser

shell:
	python manage.py shell
