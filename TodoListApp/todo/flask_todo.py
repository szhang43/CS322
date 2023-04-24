"""
Web based to-do list.

CS 322 - University of Oregon

Author: Ali Hassani
"""
import os
import logging

import flask
from flask import request

from pymongo import MongoClient

# Set up Flask app
app = flask.Flask(__name__)
app.debug = True
app.logger.setLevel(logging.DEBUG)

# Set up MongoDB connection
client = MongoClient('mongodb://' + os.environ['MONGODB_HOSTNAME'], 27017)

# Use database "todo"
db = client.todo

# Use collection "lists" in the databse
collection = db.lists


##################################################
################ MongoDB Functions ############### 
##################################################


def get_todo():
    """
    Obtains the newest document in the "lists" collection in database "todo".

    Returns title (string) and items (list of dictionaries) as a tuple.
    """
    # Get documents (rows) in our collection (table),
    # Sort by primary key in descending order and limit to 1 document (row)
    # This will translate into finding the newest inserted document.

    lists = collection.find().sort("_id", -1).limit(1)

    # lists is a PyMongo cursor, which acts like a pointer.
    # We need to iterate through it, even if we know it has only one entry:
    for todo_list in lists:
        # We store all of our lists as documents with two fields:
        ## title: string # title of our to-do list
        ## items: list   # list of items:

        ### every item has two fields:
        #### desc: string   # description
        #### priority: int  # priority
        return todo_list["title"], todo_list["items"]


def insert_todo(title, items):
    """
    Inserts a new to-do list into the database "todo", under the collection "lists".
    
    Inputs a title (string) and items (list of dictionaries)

    Returns the unique ID assigned to the document by mongo (primary key.)
    """
    output = collection.insert_one({
        "title": title,
        "items": items})
    _id = output.inserted_id # this is how you obtain the primary key (_id) mongo assigns to your inserted document.
    return str(_id)


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
    print("Opening for global access on port 5000")
    app.run(port=5000, host="0.0.0.0")
