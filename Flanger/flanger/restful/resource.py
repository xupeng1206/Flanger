from .exceptions import MethodNotImplement, UrlNotFound
from flask import send_file
import os


class SmartResource:

    def get(self, *args, **kwargs):
        raise MethodNotImplement

    def post(self, *args, **kwargs):
        raise MethodNotImplement

    def put(self, *args, **kwargs):
        raise MethodNotImplement

    def delete(self, *args, **kwargs):
        raise MethodNotImplement


class SwaggerResource:

    def get(self, debug, *args, **kwargs):
        if debug:
            import flanger
            return send_file(os.path.join(flanger.__swagger__, 'swagger_index.html'))
        else:
            raise UrlNotFound
