include .env

.PHONY: publish, deploy

default: configs

initialize_venv:
	python3 -m venv venv
	. venv/bin/activate
	pip3 install -r requirements.txt

configs: initialize_venv
	python3 scripts/config_gen.py

build: configs
	docker compose build

up: build
	docker compose up --remove-orphans

down:
	docker compose down

push: build
	docker compose push

load_sdl: configs
	cp akash-sdl.yml ../infra/akash/docker/terraform/akash-sdl.yml

deploy:
	$(MAKE) publish VERSION_TYPE=$(VERSION_TYPE)
	$(MAKE) push
	cp akash-sdl.yml ../infra/akash/docker/terraform/akash-sdl.yml
	cd ../infra/akash/docker && docker compose build akash-deploy && docker compose down && docker compose up akash-deploy

destroy:
	cd ../infra/akash/docker && docker compose down && docker compose up akash-destroy

increment_patch:
	python3 scripts/increment_version.py PATCH

publish:
	git diff-index --quiet HEAD
	NEW_VERSION=$$(python3 scripts/increment_version.py $(VERSION_TYPE)); \
	$(MAKE) configs; \
	git add .; \
	git commit -m "Release $(VERSION_TYPE) version $$NEW_VERSION"; \
	git tag -a "$$NEW_VERSION" -m "Version $$NEW_VERSION"; \
	git push origin main; \
	git push origin "$$NEW_VERSION"; \
	$(MAKE) push