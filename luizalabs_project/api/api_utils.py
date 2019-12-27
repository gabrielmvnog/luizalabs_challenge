from functools import wraps
from flask import request
import jwt
from loguru import logger
import os


class Response():
    """ An helper to manage all the mensages from the API """

    @staticmethod
    def custom(body):
        return dict(status='Success', **body)

    @staticmethod
    def error():
        return dict(status='Internal Error')

    @staticmethod
    def parameters_error():
        return dict(message='Parameters Error')

    @staticmethod
    def autorization_error():
        return dict(message='Not autorized, please authenticate')

    @staticmethod
    def login_error():
        return dict(message='Login error')


def verify_auth(function):
    """
    An decorator to authenticate an user and autorize to use the API.

    PARAMETERS
    ----------
        - A function of the Rest API.
    RETURN
    ------
        - If autorized return the function to finish it process, else it return
        an message.
    """

    wraps(function)

    def wrapper(*args, **kwargs):
        if request.authorization:
            try:
                user = request.authorization['username']
                password = request.authorization['password']

                if user == os.environ.get('API_USER') \
                        and password == os.environ.get('API_PASS'):
                    return function(*args, **kwargs)
                else:
                    return Response.login_error()

            except (jwt.exceptions.DecodeError, jwt.ExpiredSignatureError):
                logger.exception("Autorization error !!!")

                return Response.autorization_error()

        else:
            return Response.autorization_error()

    return wrapper
