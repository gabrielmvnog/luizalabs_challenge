from luizalabs_project.api.customer_api import CustomerAPI

def add_resources(api_flask):
    api_flask.add_resource(CustomerAPI, '/api/customer')