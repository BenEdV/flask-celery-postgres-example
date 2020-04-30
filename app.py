from flask import Flask
from celery import Celery
from flask_sqlalchemy import SQLAlchemy
import redis

import psycopg2
import time

# Add Redis URL configurations
app = Flask(__name__)

app.config["CELERY_BROKER_URL"] = "redis://redis:6379/0"
app.config["CELERY_RESULT_BACKEND"] = "redis://redis:6379/0"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://user:password@postgresdb:5432/db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Wait for postgres container
while(True):
    try:
        conn = psycopg2.connect(app.config["SQLALCHEMY_DATABASE_URI"])
        print("Postgres connection established")
        break
    except:
        time.sleep(1)
        print("Waiting for postgres...")

#######################
# Redis configuration #
#######################
# Connect Redis db
redis_db = redis.Redis(
    host="redis",
    port="6379",
    db=1,
    charset="utf-8",
    decode_responses=True
)

# Initialize Celery and update its config
celery = Celery(app.name)
celery.conf.update(
    result_backend=app.config["CELERY_RESULT_BACKEND"],
    broker_url=app.config["CELERY_BROKER_URL"],
    timezone="UTC",
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json"
)

##########################
# Postgres configuration #
##########################
# Postgres
db = SQLAlchemy(app)

class Node(db.Model):
    __tablename__ = 'node'
    id = db.Column(db.Integer, primary_key=True)
    visits = db.Column(db.Integer)

db.create_all()

#######################
# Flask configuration #
#######################
# Views
@app.route("/")
def index_view():
    return "Flask-celery task scheduler with postgres!"

@app.route("/node/<int:node_id>")
def node_view(node_id):
    node = Node.query.get(node_id)
    if node is None:
        return "Node is not yet created!"
    inc_node.delay(node_id)
    return f"Node {node.id} has been visited: {node.visits} times"

@app.route("/node")
def new_node_view():
    create_node.delay()
    return f"Created new node. Please wait 10 seconds to visit the node :)"

# Tasks
@celery.task
def create_node():
    node = Node()
    node.visits = 0
    time.sleep(10)
    db.session.add(node)
    db.session.commit()

@celery.task
def inc_node(node_id):
    node = Node.query.get(node_id)
    node.visits += 1
    db.session.commit()

# Run server
if __name__ == "__main__":
    app.run()
