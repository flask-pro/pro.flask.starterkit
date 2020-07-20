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

# Testing.
test_start: reset
	# Run database for tests.
	docker-compose -f docker-compose.yml up -d --build

test_run:
	# Run pytest.
	./venv/bin/pytest --cov=nucleus tests/

test: test_start test_run reset
	# Run tests.
	echo Test finished!

test_end:
	# Run tests.
	docker-compose -f docker-compose.yml down --volumes

# Running.
run: test_start
	# Run application for development.
	export PYTHONPATH=$$PYTHONPATH:nucleus; ./venv/bin/python nucleus/main.py

run_test_instance: reset
	# Run project in docker containers
	docker-compose -f docker-compose.stage.yml up --build
