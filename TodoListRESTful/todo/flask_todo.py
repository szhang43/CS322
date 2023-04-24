"""
Web based to-do list with RESTful API.

CS 322 - University of Oregon

Author: Ali Hassani
"""
import os
import logging
import requests # The library we use to send requests to the API
# Not to be confused with flask.request.
import flask
from flask import request

# Set up Flask app
app = flask.Flask(__name__)
app.debug = True if "DEBUG" not in os.environ else os.environ["DEBUG"]
port_num = True if "PORT" not in os.environ else os.environ["PORT"]
app.logger.setLevel(logging.DEBUG)


##################################################
################### API Callers ################## 
##################################################

API_ADDR = os.environ["API_ADDR"]
API_PORT = os.environ["API_PORT"]
API_URL = f"http://{API_ADDR}:{API_PORT}/api/"

def get_todo():
    """
    Obtains the newest document in the "lists" collection in database
    by calling the RESTful API.

    Returns title (string) and items (list of dictionaries) as a tuple.
    """
    # Get documents (rows) in our collection (table),
    # Sort by primary key in descending order and limit to 1 document (row)
    # This will translate into finding the newest inserted document.

    lists = requests.get(f"{API_URL}/todolists").json()

    # lists should be a list of dictionaries.
    # we just need the last one:
    todolist = lists[-1]
    return todolist["title"], todolist["items"]


def insert_todo(title, items):
    """
    Inserts a new to-do list into the database by calling the API.
    
    Inputs a title (string) and items (list of dictionaries)
    """
    _id = requests.post(f"{API_URL}/todolists", json={"title": title, "items": items}).json()
    return _id


##################################################
################## Flask routes ################## 
##################################################


@app.route("/")
def index():
    """
    Shows the home page.

    HTML interface: responds with an HTML.
    """
    return flask.render_template('todolist.html')


@app.route("/insert", methods=["POST"])
def insert():
    """
    /insert : inserts a to-do list into the database.

    Accepts POST requests ONLY!

    JSON interface: gets JSON, responds with JSON
    """
    try:
        # Read the entire request body as a JSON
        # This will fail if the request body is NOT a JSON.
        input_json = request.json
        # if successful, input_json is automatically parsed into a python dictionary!
        
        # Because input_json is a dictionary, we can do this:
        title = input_json["title"] # Should be a string
        items = input_json["items"] # Should be a list of dictionaries

        todo_id = insert_todo(title, items)

        return flask.jsonify(result={},
                        message="Inserted!", 
                        status=1, # This is defined by you. You just read this value in your javascript.
                        mongo_id=todo_id)
    except:
        # The reason for the try and except is to ensure Flask responds with a JSON.
        # If Flask catches your error, it means you didn't catch it yourself,
        # And Flask, by default, returns the error in an HTML.
        # We want /insert to respond with a JSON no matter what!
        return flask.jsonify(result={},
                        message="Oh no! Server error!", 
                        status=0, 
                        mongo_id='None')


@app.route("/fetch")
def fetch():
    """
    /fetch : fetches the newest to-do list from the database.

    Accepts GET requests ONLY!

    JSON interface: gets JSON, responds with JSON
    """
    try:
        title, items = get_todo()
        return flask.jsonify(
                result={"title": title, "items": items}, 
                status=1,
                message="Successfully fetched a to-do list!")
    except:
        return flask.jsonify(
                result={}, 
                status=0,
                message="Something went wrong, couldn't fetch any lists!")


##################################################
################# Start Flask App ################ 
##################################################


if __name__ == "__main__":
    app.run(port=port_num, host="0.0.0.0")
