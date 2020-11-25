create_venv:
	# Create virtual environment.
	python3.8 -m venv venv
	./venv/bin/pip3 install --upgrade pip
	./venv/bin/pip3 install --upgrade setuptools
	./venv/bin/pip3 install wheel
	./venv/bin/pip3 install -r requirements-dev.txt

reset:
	# Reset all conteiners create in project.
	echo "" > .env
	docker-compose -f docker-compose.dev.yml down --volumes --remove-orphans
	docker-compose -f docker-compose.staging.yml down --volumes --remove-orphans
	rm -rf .env staging.tmp staging.zip

test_containers_start: reset
	# Run container with database.
	docker-compose -f docker-compose.dev.yml up -d --build

test: reset
	# Run pytest.
	./venv/bin/pytest --cov=nucleus tests/

# Running.
run: test_containers_start
	# Run application for development.
	sh run_nucleus.sh dev.env

build_staging_release: reset
	docker build nucleus -t nucleus
	docker save nucleus:latest > testing.tmp
	cp staging.env .env
	unzip -p staging.env.zip >> .env
	zip -r staging.zip docker-compose.staging.yml .env staging.tmp grafana nginx prometheus

run_staging_instance: build_staging_release
	# Run project in docker containers
	docker-compose -f docker-compose.staging.yml up

format:
	# Run checking and formatting sources.
	./venv/bin/pre-commit run -a
