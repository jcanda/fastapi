#!/bin/bash

DOCKER_FASTAPI = fast-api-web-1
UID := $(shell id -u)

help: ## Show this help message
	@echo 'usage: make [target]'
	@echo
	@echo 'targets:'
	@egrep '^(.+)\:\ ##\ (.+)' ${MAKEFILE_LIST} | column -t -c 2 -s ':#'

run: ## Start the containers
	U_ID=${UID} docker-compose up -d

stop: ## Stop the containers
	U_ID=${UID} docker-compose stop

restart: ## Restart the containers
	$(MAKE) stop && $(MAKE) run

build: ## Rebuilds all the containers
	U_ID=${UID} docker-compose build


migrate-test: ## Test alembic migrations
	U_ID=${UID} docker exec -it --user ${UID} ${DOCKER_FASTAPI} alembic current

migrate-create:  ## Create new alembic database migration aka database revision. Usage: make migrate-create msg="your message"
	U_ID=${UID} docker exec -it --user ${UID} ${DOCKER_FASTAPI} alembic revision --autogenerate -m "$(msg)"

migrate-apply: ## apply alembic migrations to database/schema
	U_ID=${UID} docker exec -it --user ${UID} ${DOCKER_FASTAPI} alembic upgrade head

migrate-downgrade: ## downgrade alembic migrations to database/schema
	U_ID=${UID} docker exec -it --user ${UID} ${DOCKER_FASTAPI} alembic downgrade base

migrate-downgrade-1: ## downgrade alembic migrations to database/schema by 1
	U_ID=${UID} docker exec -it --user ${UID} ${DOCKER_FASTAPI} alembic downgrade -1

migrate-history: ## list alembic migration history
	U_ID=${UID} docker exec -it --user ${UID} ${DOCKER_FASTAPI} alembic history

logs-web: ## Tails the logs
	U_ID=${UID} docker-compose logs web -f

logs: ## Tails log
	U_ID=${UID} docker exec -it --user ${UID} ${DOCKER_FASTAPI} tail -f /var/log/*.log

ssh: ## ssh's into the be container
	U_ID=${UID} docker exec -it --user ${UID} ${DOCKER_FASTAPI} bash

clean: ## Clean __pycache__ files
	find . -name "__pycache__" -type d -exec rm -rf {} + -o -name "*.pyc" -type f -exec rm -f {} +

pre-commit: ## Run pre-commit
	pre-commit run --all-files

dump: ## Dump
	mkdir -p backups
	rm -fr backups/*
	mysqldump -h 127.0.0.1 -u mysqldbu -pmysqlpass mysqldb > backups/fastapi.sql

restore: ## Restore
	U_ID=${UID} docker-compose stop web
	U_ID=${UID} docker-compose exec db mysql -u mysqldbu -pmysqlpass mysqldb < tools/init.sql
	U_ID=${UID} docker-compose exec db mysql -u mysqldbu -pmysqlpass mysqldb < backups/fastapi.sql
	U_ID=${UID} docker-compose up -d

.PHONY: help Makefile
