from flasgger import Swagger
from flask import Flask
from flask_restful import Api

from luizalabs_project.api import add_resources

template = {
    "Swagger": "2.0",
    "info": {
        "title": "Luizalabs - Challenge",
        "description": "Development of an CRUD",
        "version": "0.0.1"
    },
    'securityDefinitions': {
        'basicAuth': {
            'type': 'basic'
        }
    },
}

app = Flask(__name__)
api_flask = Api(app)
swagger = Swagger(app=app, template=template)

add_resources(api_flask)


@app.route('/')
def index():
    return 'Api is running', 200
