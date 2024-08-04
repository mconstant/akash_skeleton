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
	# Check that git staging area is clean
	git diff-index --quiet HEAD
	python3 scripts/increment_version.py PATCH
	$(MAKE) configs
	git add .
	git commit -m "Bump version to $(shell cat VERSION)"
	# tag the commit
	git tag -a $(shell cat VERSION) -m "Version $(shell cat VERSION)"
	# push the commit and tag
	git push origin main
	git push origin $(shell cat VERSION)
	# push the image
	$(MAKE) push

publish_minor: