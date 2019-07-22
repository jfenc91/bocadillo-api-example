test:
	tox

dev: 
	uvicorn asgi:app --reload

build:
	docker build . -t api

start: 
	docker run -p 8080:8080 api

stop:
	docker rm -f api
