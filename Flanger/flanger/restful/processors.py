from .response import FlangerResponse
from .exceptions import FlangerError, UrlNotFound, MethodNotImplement
from .resource import SwaggerResource
from .utils import extract_params
from flask import send_file
import os
import logging

logger = logging.getLogger(__name__)


class BaseRequestProcessor:

    def __init__(self, app, *args, **kwargs):
        self.app = app

    def process_request(self, request, *args, **kwargs):
        try:
            url_rule = request.url_rule
            if not url_rule:
                raise UrlNotFound

            resource = self.app.endpoint_resource[url_rule.endpoint] if url_rule.endpoint in self.app.endpoint_resource else None
            if resource is None:
                raise UrlNotFound

            request_method = request.method.lower()
            method = getattr(resource, request_method, None)
            if method is None:
                raise MethodNotImplement

            params = {'request': request}
            ret_params = extract_params(request)
            if isinstance(ret_params, dict):
                params.update(ret_params)

            if url_rule.endpoint == 'Base.SwaggerResource':
                params.update({'debug': self.app.config['DEBUG']})

            data = method(**params)

            if url_rule.endpoint == 'Base.SwaggerResource':
                return data

            return FlangerResponse.success(data if not data is None else {})

        except FlangerError as e:
            logger.error(e.msg)
            return FlangerResponse.error(e.code, e.msg)
        except Exception as e:
            raise e


class BaseResponseProcessor:

    def __init__(self, app, *args, **kwargs):
        self.app = app

    def process_response(self, response):
        return response


class FlangerSwaggerProcessor:

    def __init__(self, app, *args, **kwargs):
        self.app = app

    def process_request(self, request, *args, **kwargs):
        try:
            url_rule = request.url_rule
            if not url_rule:
                raise UrlNotFound

            resource = SwaggerResource()

            request_method = request.method.lower()
            method = getattr(resource, request_method, None)
            if method is None:
                raise MethodNotImplement

            params = {'request': request, 'debug': self.app.config['DEBUG']}
            ret_params = extract_params(request)
            if isinstance(ret_params, dict):
                params.update(ret_params)

            data = method(**params)
            return data

        except FlangerError as e:
            logger.error(e.msg)
            return FlangerResponse.error(e.code, e.msg)
        except Exception as e:
            raise e


class FlangerStaticProcessor:

    def __init__(self, app, *args, **kwargs):
        self.app = app

    def process(self, request, *args, **kwargs):
        import flanger
        if request.path.strip('/') == 'favicon.ico':
            return send_file(os.path.join(flanger.__swagger__, 'favicon-32x32.png'))
        params = {'request': request}
        ret_params = extract_params(request)
        if isinstance(ret_params, dict):
            params.update(ret_params)
        filepath = params['filepath']
        if filepath == 'swagger.json':
            swagger_json_path = os.path.join(os.path.join(self.app.config['BASE_DIR'], 'static'), 'swagger.json')
            return send_file(swagger_json_path)
        return send_file(os.path.join(flanger.__swagger__, filepath))
