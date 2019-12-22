import json
from flask import request
import bson
from bson import json_util
from flasgger import swag_from
from flask_restful import Resource


from luizalabs_project.modules.databases import CustomerDB
from luizalabs_project.api.api_utils import Response, verify_auth


class CustomersListAPI(Resource):

    @swag_from('docs/customersListAPI_get.yml')
    @verify_auth
    def get(self):
        database = CustomerDB()

        try:
            return json.loads(json_util.dumps(database.show_all()))
        except bson.errors.InvalidId:
            return Response.parameters_error()


class CustomerListAPI(Resource):
    @swag_from('docs/customerListAPI_get.yml')
    @verify_auth
    def get(self, customer_id):
        database = CustomerDB()

        try:
            return json.loads(json_util.dumps(database.show_one(customer_id)))
        except bson.errors.InvalidId:
            return Response.parameters_error()

class CustomerAPI(Resource):

    @swag_from('docs/customerAPI_post.yml')
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

    @swag_from('docs/customerAPI_put.yml')
    @verify_auth
    def put(self):
        req = request.json
        database = CustomerDB()

        try:
            object_id = req['object_id']
            name = req['name'] if 'name' in req.keys() else None
            email = req['email'] if 'email' in req.keys() else None

            result = database.update(object_id, name, email)

            message = "Customer updated with success" \
                if result else "Couldn't update the user, email already in use"

            return Response.custom(dict(message=message))

        except (KeyError, TypeError):
            return Response.parameters_error()

        return Response.error()

    @swag_from('docs/customerAPI_delete.yml')
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
