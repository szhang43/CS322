"""
Brevets RESTful API
"""
import logging
import os
from flask import Flask
from flask_restful import Api
from mongoengine import connect

from resources.todolist import TodoListResource
from resources.todolists import TodoListsResource

# Connect MongoEngine to mongodb
connect(host=f"mongodb://{os.environ['MONGODB_HOSTNAME']}:27017/brevetsdb")

# Start Flask app and Api here:
app = Flask(__name__)
app.debug = True if "DEBUG" not in os.environ else os.environ["DEBUG"]
port_num = True if "PORT" not in os.environ else os.environ["PORT"]
app.logger.setLevel(logging.DEBUG)
api = Api(app)

# Bind resources to paths here:
api.add_resource(TodoListResource, "/api/todolist/<id>")
api.add_resource(TodoListsResource, "/api/todolists")

if __name__ == "__main__":
    # Run flask app normally
    app.run(port=port_num, host="0.0.0.0")
