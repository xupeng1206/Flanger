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
            flanger_path = os.path.dirname(flanger.__file__)
            index_path = os.path.join(os.path.join(flanger_path, 'swagger'), 'swagger_index.html')
            return send_file(index_path)
        else:
            raise UrlNotFound
