network:
	docker network create flask-by-example

postgres:
	docker run -d --rm \
  --name postgres \
  --network flask-by-example \
  -p 5432:5432 \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=adminSecret \
  -e POSTGRES_DB=flask-by-example \
  -v postgres-data:/var/lib/postgresql/data \
  postgres

pgadmin4:
	docker run -d --rm \
  --name pgadmin4 \
  --network flask-by-example \
  -p 8000:80 \
  -e PGADMIN_DEFAULT_EMAIL=admin@example.com \
  -e PGADMIN_DEFAULT_PASSWORD=adminSecret \
  -v pgadmin-data:/var/lib/pgadmin \
  dpage/pgadmin4

redis:
	docker run -d --rm --name redis -p 6379:6379 -d redis:7-alpine

createdb:
	docker exec -it postgres createdb --username=admin --owner=admin flask-by-example

stopdb:
	docker stop postgres pgadmin4

startTestEnv:
	@$(MAKE) postgres
	@sleep 2
	@$(MAKE) pgadmin4
	@sleep 2
	@$(MAKE) redis

stopTestEnv:
	docker stop postgres pgadmin4 redis

server:
	flask run

worker:
	python worker.py

migrateInit:
	rm -rf migrations
	python manage.py db init
	python manage.py db migrate -m "Initial migration"

migrate:
	python manage.py db upgrade

.PHONY: startTestEnv stopTestEnv network postgres createdb redis stopdb setEnvVars server migrateInit migrate
