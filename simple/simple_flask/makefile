enironment_init:
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt
	echo "FLASK_APP=main" >> .env
	echo "FLASK_ENV=development" >> .env
	echo "FLASK_DEBUG=1" >> .env

run:
	./venv/bin/flask run

testing:
	./venv/bin/pytest -s

coverage:
	./venv/bin/pytest --cov=simple_flask tests/