.PHONY: build, re-build, up, down, list, logs, test, makemigrations, coverage


DOCKER_VERSION := $(shell docker --version 2>/dev/null)
DOCKER_COMPOSE_VERSION := $(shell docker-compose --version 2>/dev/null)


all:
ifndef DOCKER_VERSION
    $(error "command docker is not available, please install Docker")
endif
ifndef DOCKER_COMPOSE_VERSION
    $(error "command docker-compose is not available, please install Docker")
endif

re-build:
	docker-compose build --no-cache

build:
	docker-compose build

up:
	docker network inspect web >/dev/null 2>&1 || \
		docker network create web
	docker-compose up -d

down:
	docker-compose down

list:
	docker-compose ps

logs:
	docker-compose logs

makemigrations:up
	@docker exec web bash -c 'python manage.py makemigrations'

test: up
	@docker exec web bash -c 'pytest'

coverage: up
	@docker exec web bash -c 'coverage run -m pytest && coverage report'
