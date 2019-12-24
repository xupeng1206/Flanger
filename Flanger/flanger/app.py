from flask import Flask, request
from .restful.processors import BaseRequestProcessor, BaseResponseProcessor, FlangerStaticProcessor, \
    FlangerSwaggerProcessor
from .restful.urls import FlangerUrls
from .restful.utils import extract_clz_from_string
from .restful.swagger import generate_swagger_json
from flanger.db.models.base import db
import logging

logger = logging.getLogger(__name__)


class FlangerApp(Flask):
    endpoint_resource = {}
    endpoint_url = {}
    request_processors = []
    response_processors = []
    flanger_static_processor = None
    flanger_swagger_processor = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def init(self):
        self.init_db()
        self.init_urls()
        self.init_swagger()
        self.init_request_processors()
        self.init_response_processors()
        self.before_request(self.bind_processor)

    def init_db(self):
        pass
        # db.create_all(app=self)

    def init_urls(self):

        if 'FLANGER_URLS' in self.config:
            if isinstance(self.config['FLANGER_URLS'], list):
                for urls in self.config['FLANGER_URLS']:
                    clz = extract_clz_from_string(urls)

                    prefix = ''
                    if hasattr(clz, 'url_prefix'):
                        prefix = f'/{clz.url_prefix.strip("/")}'

                    for url, resource in clz.urls.items():
                        url = f'{prefix}/{url.strip("/")}'
                        # 产生allowed_methods
                        allowed = []
                        for method in ['get', 'post', 'put', 'delete']:
                            if hasattr(resource, method):
                                allowed.append(method)
                        resource.allowed_methods = allowed
                        ep = f'{clz.__module__}.{clz.__name__}.{resource.__name__}'
                        self.add_url_rule(url, endpoint=ep, methods=['GET', 'POST', 'PUT', 'DELETE'])
                        self.endpoint_resource[ep] = resource()
                        self.endpoint_url[ep] = url
            else:
                raise Exception('FLANGER_URLS must be list !!!')

        self.add_url_rule('/fstatic/<filepath>', endpoint='fstatic', methods=['GET'])

    def init_swagger(self):

        self.add_url_rule('/favicon.ico', endpoint='favicon')
        for url, resource in FlangerUrls.urls.items():
            self.add_url_rule(url, endpoint='fswagger')

        self.flanger_swagger_processor = FlangerSwaggerProcessor(self)
        self.flanger_static_processor = FlangerStaticProcessor(self)

        if 'BASE_DIR' not in self.config:
            raise Exception('BASE_DIR must in settings !!!')
        generate_swagger_json(self)

    def init_request_processors(self):
        if 'FLANGER_REQUEST_PROCESSORS' in self.config:
            if not isinstance(self.config['FLANGER_REQUEST_PROCESSORS'], list):
                raise Exception('FLANGER_REQUEST_PROCESSORS must be list !!!')
            else:
                for processor in self.config['FLANGER_REQUEST_PROCESSORS']:
                    clz = extract_clz_from_string(processor)
                    if clz in BaseRequestProcessor.__subclasses__():
                        self.request_processors.append(clz(self))
                    else:
                        def __init__(self, app, *args, **kwargs):
                            self.app = app

                        clz.__init__ = __init__

                        self.request_processors.append(clz(self))

    def init_response_processors(self):
        if 'FLANGER_RESPONSE_PROCESSORS' in self.config:
            if not isinstance(self.config['FLANGER_RESPONSE_PROCESSORS'], list):
                raise Exception('FLANGER_RESPONSE_PROCESSORS must be list !!!')
            else:
                for processor in self.config['FLANGER_RESPONSE_PROCESSORS']:
                    clz = extract_clz_from_string(processor)

                    if clz in BaseResponseProcessor.__subclasses__():
                        self.response_processors.append(clz(self))
                    else:
                        def __init__(self, app, *args, **kwargs):
                            self.app = app

                        clz.__init__ = __init__
                        self.response_processors.append(clz(self))

    def bind_processor(self):
        # flanger 自身的static
        url_rule = request.url_rule

        if url_rule.endpoint.strip('/') == 'fswagger':
            return self.flanger_swagger_processor.process_request(request)

        if url_rule.endpoint.strip('/') in ['fstatic', 'favicon']:
            return self.flanger_static_processor.process(request)

        # 静态文件不走flanger逻辑，走flask原本的逻辑
        if url_rule.endpoint.strip('/') == self.static_url_path.strip('/'):
            return

        for processor in self.request_processors:
            if hasattr(processor, 'process_request'):
                response = processor.process_request(request)
                if response:
                    return response

        response = BaseRequestProcessor(self.endpoint_resource).process_request(request)
        for processor in self.response_processors:
            if hasattr(processor, 'process_response'):
                response = processor.process_response(response)
        return response
