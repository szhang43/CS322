"""
Resource: TodoListsResource
"""
from flask import Response, request
from flask_restful import Resource

from database.models import TodoList

class TodoListsResource(Resource):
    def get(self):
        json_object = TodoList.objects().to_json()
        return Response(json_object, mimetype="application/json", status=200)

    def post(self):
        # Read the entire request body as a JSON
        # This will fail if the request body is NOT a JSON.
        input_json = request.json

        ## Because input_json is a dictionary, we can do this:
        #title = input_json["title"] # Should be a string
        #items = input_json["items"] # Should be a list of dictionaries
        #result = TodoList(title=title, items=items).save()

        result = TodoList(**input_json).save()
        return {'_id': str(result.id)}, 200
