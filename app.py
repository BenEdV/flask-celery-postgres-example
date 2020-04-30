from flask import Flask
from celery import Celery
from celery.utils.log import get_task_logger
import redis

logger = get_task_logger(__name__)
app = Flask(__name__)

# Add Redis configs
app.config["CELERY_BROKER_URL"] = "redis://redis:6379/0"
app.config["CELERY_RESULT_BACKEND"] = "redis://redis:6379/0"

# Connect Redis db
redis_db = redis.Redis(
    host="redis", port="6379", db=1, charset="utf-8", decode_responses=True
)

# Initialize Celery and update its config
celery = Celery(app.name)
celery.conf.update(
    result_backend=app.config["CELERY_RESULT_BACKEND"],
    broker_url=app.config["CELERY_BROKER_URL"],
    timezone="UTC",
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)

@app.route("/")
def index_view():
    return "Flask-celery task scheduler with Postgres database!"

@celery.task
def create_node():
    pass

if __name__ == "__main__":
    app.run()
