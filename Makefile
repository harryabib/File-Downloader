.PHONY: build up down restart logs test clean

build:
	docker-compose build

up:
	docker-compose up -d app

down:
	docker-compose down

restart: down build up

logs:
	docker-compose logs -f app

test:
	docker-compose run --rm test

clean:
	docker-compose down -v --rmi all --remove-orphans