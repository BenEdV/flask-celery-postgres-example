#!/bin/sh

# Run Celery worker
#celery -A app.tasks.celery worker --loglevel=INFO --detach --pidfile=''

flask run --host=0.0.0.0 --port 5000
