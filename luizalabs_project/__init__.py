from flask import Flask
from flask_restful import Api

from luizalabs_project.api import add_resources

app = Flask(__name__)
api_flask = Api(app)

add_resources(api_flask)


