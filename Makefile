.PHONY: help build up down restart logs clean test demo

help:
	@echo "Deception & Threat Intelligence Honeypot Platform Commands:"
	@echo "  make build    - Build all container images"
	@echo "  make up       - Start all platform services in the background"
	@echo "  make down     - Stop all running platform services"
	@echo "  make restart  - Restart all services"
	@echo "  make logs     - Follow logs from all running containers"
	@echo "  make clean    - Stop containers and remove volumes"
	@echo "  make test     - Run test suite"
	@echo "  make demo     - Run automated synthetic attack script"

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

restart:
	docker compose restart

logs:
	docker compose logs -f

clean:
	docker compose down -v --remove-orphans

test:
	pytest tests/

demo:
	python scripts/generate_demo_events.py
