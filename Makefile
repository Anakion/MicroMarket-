  up:
	docker compose -f docker-compose.yml up -d

down:
	docker compose -f docker-compose.yml down --volumes && docker network prune --force
