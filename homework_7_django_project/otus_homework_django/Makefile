# Makefile
.PHONY: build up down restart shell migrate createsuperuser

build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose down

restart:
	make down && make up

shell:
	docker-compose exec web sh

migrate:
	docker-compose exec web python manage.py migrate

createsuperuser:
	docker-compose exec web python manage.py createsuperuser
