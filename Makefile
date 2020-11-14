create_venv:
	# Create virtual environment.
	python3.8 -m venv venv
	./venv/bin/pip3 install --upgrade pip
	./venv/bin/pip3 install --upgrade setuptools
	./venv/bin/pip3 install -r requirements-dev.txt

reset:
	# Reset all conteiners create in project.
	echo "" > .env
	docker-compose -f docker-compose.dev.yml down --volumes --remove-orphans
	docker-compose -f docker-compose.stage.yml down --volumes --remove-orphans

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

run_stage_instance: reset
	# Run project in docker containers
	docker build nucleus -t nucleus
	cp stage.env .env
	unzip -p stage.env.zip >> .env
	docker-compose -f docker-compose.stage.yml up

log_stage_instance:
	docker logs stage_app

format:
	# Run checking and formatting sources.
	./venv/bin/pre-commit run -a
