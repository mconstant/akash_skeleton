include .env

default: configs

initialize_venv:
	python3 -m venv venv
	. venv/bin/activate
	pip install -r requirements.txt

configs:
	python3 scripts/config_gen.py

build: configs
	docker compose build

up: build
	docker compose up --remove-orphans

down:
	docker compose down

push: build
	docker compose push

load_sdl: push

deploy: push
	cd ../infra/akash/docker && docker compose 

publish_patch:
	git diff-index --quiet HEAD
	NEW_VERSION=$$(python3 scripts/increment_version.py PATCH); \
	$(MAKE) configs; \
	git add .; \
	git commit -m "Bump version to $$NEW_VERSION"; \
	git tag -a "$$NEW_VERSION" -m "Version $$NEW_VERSION"; \
	git push origin main; \
	git push origin "$$NEW_VERSION"; \
	$(MAKE) push

publish_minor: