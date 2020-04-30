## Flask Celery Postgres Example

This is minimal example of a [flask](https://flask.palletsprojects.com/en/1.1.x/) app using [Celery](http://www.celeryproject.org) for background tasks and a [Postgres](https://www.postgresql.org) database that is accessed by flask and celery.

#### Instructions
To run the application use
```sh
docker-compose up --build
```
Access database
```sh
dc exec postgresdb psql -U user -d db
```
