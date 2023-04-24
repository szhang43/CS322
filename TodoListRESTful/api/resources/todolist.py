"""
Resource: TodoListResource
"""
from flask import Response, request
from flask_restful import Resource

from database.models import TodoList

class TodoListResource(Resource):
    def get(self, id):
        brevet = TodoList.objects.get(id=id).to_json()
        return Response(brevet, mimetype="application/json", status=200)

    def put(self, id):
        input_json = request.json
        TodoList.objects.get(id=id).update(**input_json)
        return '', 200

    def delete(self, id):
        TodoList.objects.get(id=id).delete()
        return '', 200
