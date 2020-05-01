#!/bin/sh

# Run Celery worker
celery -A app.celery worker --loglevel=INFO --logfile=celery.log --detach --pidfile=''

flask run --host=0.0.0.0 --port 5000
