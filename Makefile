.PHONY: help install test run

help:
	@echo "Comandos disponíveis: install, test, run, docker-up"

install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install

test:
	cd backend && pytest tests/ -v

run:
	docker-compose up

docker-up:
	docker-compose up -d
