build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose down

run:
	docker-compose up

migration:
	docker compose run --rm web alembic revision --autogenerate

migrate:
	docker compose run --rm web alembic upgrade head

test:
	(docker compose run --rm web coverage run -m pytest);
	(docker compose run --rm web coverage run -m coverage report);

initialize:
	docker compose run --rm web python init_data.py
