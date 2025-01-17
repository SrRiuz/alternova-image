build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose down

run:
	docker-compose up

test:
	(docker compose run --rm web coverage run -m pytest);
	(docker compose run --rm web coverage run -m coverage report);

