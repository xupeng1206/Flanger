from flanger.restful.exceptions import MethodNotImplement


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

    def get(self, *args, **kwargs):
        return {'data': 'swagger'}