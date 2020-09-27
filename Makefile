create_venv:
	# Create virtual environment.
	python3.8 -m venv venv
	./venv/bin/pip3 install --upgrade pip
	./venv/bin/pip3 install --upgrade setuptools
	./venv/bin/pip3 install -r requirements-dev.txt

reset:
	# Reset all conteiners create in project.
	docker-compose -f docker-compose.yml down --volumes --remove-orphans
	docker-compose -f docker-compose.stage.yml down --volumes --remove-orphans

run_db: reset
	# Run container with database.
	docker-compose -f docker-compose.yml up -d --build

test:
	# Run pytest.
	./venv/bin/pytest --cov=nucleus tests/

# Running.
run: run_db
	# Run application for development.
	export PYTHONPATH=$$PYTHONPATH:nucleus; ./venv/bin/python nucleus/main.py

run_test_instance: reset
	# Run project in docker containers
	docker-compose -f docker-compose.stage.yml up --build

format:
	# Run checking and formatting sources.
	./venv/bin/pre-commit run -a
