from functools import wraps
from flask import request
import jwt


class Response():

    @staticmethod
    def custom(body):
        return dict(status='Success', **body)

    @staticmethod
    def error():
        return dict(status='Error')

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
    wraps(function)

    def wrapper(*args, **kwargs):
        if request.authorization:
            try:
                user = request.authorization['username']
                password = request.authorization['password']

                if user == "admin" and password == "admin":
                    return function(*args, **kwargs)
                else:
                    return Response.login_error()

            except (jwt.exceptions.DecodeError, jwt.ExpiredSignatureError):
                return Response.autorization_error()

        else:
            return Response.autorization_error()

    return wrapper
