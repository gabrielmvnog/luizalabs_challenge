import json
from flask import request
import bson
import pymongo
from loguru import logger
from bson import json_util
from flasgger import swag_from
from flask_restful import Resource


from luizalabs_project.modules.databases import CustomerDB
from luizalabs_project.api.api_utils import Response, verify_auth


class CustomersListAPI(Resource):

    @swag_from('docs/customersListAPI_get.yml')
    @verify_auth
    def get(self):
        logger.info("Recovering information from all customer.")

        try:
            database = CustomerDB()

            return json.loads(json_util.dumps(database.show_all()))
        except (bson.errors.InvalidId, pymongo.errors.OperationFailure):
            logger.exception("Database Failure !!!")

            return Response.error()

        return Response.error()


class CustomerListAPI(Resource):
    @swag_from('docs/customerListAPI_get.yml')
    @verify_auth
    def get(self, customer_id):
        logger.info("Recovering information from a customer.")

        try:
            database = CustomerDB()

            return json.loads(json_util.dumps(database.show_one(customer_id)))
        except (bson.errors.InvalidId, pymongo.errors.OperationFailure):
            logger.exception("Database Failure !!!")

            return Response.error()

        return Response.error()


class CustomerAPI(Resource):

    @swag_from('docs/customerAPI_post.yml')
    @verify_auth
    def post(self):
        logger.info("Adding new customer.")

        try:
            req = request.json
            name, email = req['name'], req['email']

        except (KeyError, TypeError):
            logger.exception("Parameters error !!!")

            return Response.parameters_error()

        try:
            database = CustomerDB()

            result = database.add(name, email)

            message = "Customer added with success" \
                if result else "Email already in use"

            return Response.custom(dict(message=message))

        except pymongo.errors.OperationFailure:
            logger.exception("Database Failure !!!")

            return Response.error()

        return Response.error()

    @swag_from('docs/customerAPI_put.yml')
    @verify_auth
    def put(self):
        logger.info("Updating a customer.")

        try:
            req = request.json
            customer_id = req['customer_id']
            name = req['name'] if 'name' in req.keys() else None
            email = req['email'] if 'email' in req.keys() else None

            if (not name) and (not email):
                return Response.custom(
                    dict(message='Please, update need name or '
                         'email as parameters'))

        except (KeyError, TypeError):
            logger.exception("Parameters error !!!")

            return Response.parameters_error()

        try:
            database = CustomerDB()

            result = database.update(customer_id, name, email)

            message = "Customer updated with success" \
                if result else "Couldn't update the user, email already in use"

            return Response.custom(dict(message=message))

        except pymongo.errors.OperationFailure:
            logger.exception("Database Failure !!!")

            return Response.error()

        return Response.error()

    @swag_from('docs/customerAPI_delete.yml')
    @verify_auth
    def delete(self):
        logger.info("Deleting customer.")

        try:
            req = request.json

            customer_id = req['customer_id']

        except (KeyError, TypeError):
            logger.exception("Parameters error !!!")

            return Response.parameters_error()

        try:
            database = CustomerDB()
            result = database.remove(customer_id)

            message = "Customer removed with success" \
                if result else "Couldn't remove the user"

            return Response.custom(dict(message=message))
        except pymongo.errors.OperationFailure:
            logger.exception("Database Failure !!!")

            return Response.error()

        return Response.error()
