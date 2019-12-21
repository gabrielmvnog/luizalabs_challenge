from flask import request
from flask_restful import Resource
from functools import wraps
import json
from bson import json_util

from luizalabs_project.modules.databases import CustomerDB
from luizalabs_project.api.api_utils import Response, verify_auth


class CustomerAPI(Resource):
    
    @verify_auth
    def get(self):
        database = CustomerDB()

        return json.loads(json_util.dumps(database.show_all()))

    @verify_auth
    def post(self):
        req = request.json
        database = CustomerDB()

        try:
            name, email = req['name'], req['email']

            result = database.add(name, email)

            message = "Customer added with success" \
                if result else "Email already in use"

            return Response.custom(dict(message=message))

        except (KeyError, TypeError):
            return Response.parameters_error()

        return Response.error()

    @verify_auth
    def put(self):
        req = request.json
        database = CustomerDB()

        return Response.error()

    @verify_auth
    def delete(self):
        req = request.json
        database = CustomerDB()

        try:
            object_id = req['object_id']

            result = database.remove(object_id)

            message = "Customer removed with success" \
                if result else "Couldn't remove the user"

            return Response.custom(dict(message=message))

        except (KeyError, TypeError):
            return Response.parameters_error()

        return Response.error()