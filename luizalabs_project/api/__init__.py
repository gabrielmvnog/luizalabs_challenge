from luizalabs_project.api.customer_api import (
    CustomerAPI, CustomersListAPI, CustomerListAPI)
from luizalabs_project.api.favorites_api import FavoritesAPI, FavoritesListAPI


def add_resources(api_flask):
    # Customer Endpoint
    api_flask.add_resource(CustomerAPI, '/api/customer')
    api_flask.add_resource(CustomerListAPI,
                           '/api/customer/<string:customer_id>',
                           endpoint='list_one')
    api_flask.add_resource(CustomersListAPI, '/api/customer/all')

    # Customer's favorite Endpoint
    api_flask.add_resource(
        FavoritesListAPI, '/api/favorites/<string:customer_id>')
    api_flask.add_resource(FavoritesAPI, '/api/favorite')
