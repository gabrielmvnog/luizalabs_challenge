from flasgger import swag_from
from flask_restful import Resource
from flask import request

from luizalabs_project.modules.databases import CustomerDB
from luizalabs_project.services.products import MagaluProducts
from luizalabs_project.api.api_utils import Response, verify_auth


class FavoritesListAPI(Resource):

    @verify_auth
    def get(self, customer_id):
        database = CustomerDB()

        favorites = database.get_favorites(customer_id)
        result = [MagaluProducts.check_product(
            favorite) for favorite in favorites]

        return result


class FavoritesAPI(Resource):

    @verify_auth
    def post(self):
        database = CustomerDB()

        try:
            req = request.json

            customer_id = req['customer_id']
            product_id = req['product_id']

        except KeyError:
            return Response.parameters_error()

        if MagaluProducts.check_product(product_id):

            result = database.insert_favorite(customer_id, product_id)

            if result:
                return Response.custom(dict(message="insertion with success"))
            else:
                return Response.custom(dict(message="item duplicated"))

        return Response.error()

    @verify_auth
    def delete(self):
        database = CustomerDB()

        try:
            req = request.json

            customer_id = req['customer_id']
            product_id = req['product_id']

        except KeyError:
            return Response.parameters_error()

        database.remove_favorite(customer_id, product_id)

        return Response.custom(dict(message="removed with success"))
