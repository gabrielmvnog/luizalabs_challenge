import loguru
import pymongo
from loguru import logger
from flask import request
from flasgger import swag_from
from flask_restful import Resource

from luizalabs_project.modules.databases import CustomerDB
from luizalabs_project.services.products import MagaluProducts
from luizalabs_project.api.api_utils import Response, verify_auth


class FavoritesListAPI(Resource):

    @swag_from('docs/favoritesListAPI_get.yml')
    @verify_auth
    def get(self, customer_id):
        try:
            database = CustomerDB()

            favorites = database.get_favorites(customer_id)
            result = [MagaluProducts.check_product(
                favorite) for favorite in favorites]

            return Response.custom(dict(fav_products=result))

        except pymongo.errors.OperationFailure:
            logger.exception("Database Failure !!!")

            return Response.error()


class FavoritesAPI(Resource):

    @swag_from('docs/favoritesAPI_post.yml')
    @verify_auth
    def post(self):
        logger.info("Adding favorite item to a customer.")

        try:
            req = request.json

            customer_id = req['customer_id']
            product_id = req['product_id']

        except (KeyError, TypeError):
            logger.exception("Parameters error !!!")
            
            return Response.parameters_error()

        try:
            database = CustomerDB()

            if MagaluProducts.check_product(product_id):

                result = database.insert_favorite(customer_id, product_id)

                if result:
                    return Response.custom(dict(message="insertion with success"))
                else:
                    return Response.custom(dict(message="item duplicated"))

        except pymongo.errors.OperationFailure:
            logger.exception("Database Failure !!!")

            return Response.error()


    @swag_from('docs/favoritesAPI_delete.yml')
    @verify_auth
    def delete(self):
        logger.info("Deleting favorite item to a customer.")

        try:
            req = request.json

            customer_id = req['customer_id']
            product_id = req['product_id']

        except (KeyError, TypeError):
            logger.exception("Parameters error !!!")

            return Response.parameters_error()

        try:
            database = CustomerDB()

            result = database.remove_favorite(customer_id, product_id)

            if result:
                return Response.custom(dict(message="removed with success"))
            else:
                return Response.custom(dict(message="item not found"))

        except pymongo.errors.OperationFailure:
            logger.exception("Database Failure !!!")

            return Response.error()
