default: configs

initialize_venv:
	python3 -m venv venv
	. venv/bin/activate
	pip install -r requirements.txt

configs:
	python3 config_gen.py

build: configs
	docker compose build

up: build
	docker compose up

push: build
	docker compose push

load_sdl: push
	

deploy: push
	cd ../infra/akash/docker && docker compose up