up:
	docker compose -f docker-compose.yml up -d

down:
	docker compose -f docker-compose.yml down --volumes && docker network prune --force

migrations:
	alembic init -t async app/migrations

	alembic revision --autogenerate -m "Initial migration"

	alembic upgrade head