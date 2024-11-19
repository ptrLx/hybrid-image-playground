setup:
	pipenv install --dev

start:
	pipenv run python src/main.py

start-prod:
	pipenv run gunicorn --workers=1 --chdir=src --threads=1 -b 0.0.0.0:8080 main:server

start-container:
	docker build -t hybrid-image-playground .
	docker run -it --rm -p 8080:80 hybrid-image-playground
