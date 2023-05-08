.PHONY: run

run-prod:
	gunicorn --bind 0.0.0.0:5000 app:app

run:
	FLASK_APP=app FLASK_DEBUG=1 flask run
