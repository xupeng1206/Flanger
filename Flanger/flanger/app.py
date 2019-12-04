from flask import Flask, request
from .restful.core import BaseRequestProcessor
from .restful.urls import FlangerUrls
from .restful.utils import extract_clz_from_string
import importlib


class FlangerApp(Flask):
    endpoint_resource = {}
    request_processors = []
    response_processors = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def init(self):
        self.init_db()
        self.init_urls()
        self.init_request_processors()
        self.init_response_processors()
        self.before_request(self.bind_middleware)

    def init_db(self):
        pass

    def init_urls(self):
        for url, resource in FlangerUrls.urls.items():
            ep = f'Base.{resource.__name__}'
            self.add_url_rule(url, endpoint=ep)
            self.endpoint_resource[ep] = resource()

        if 'FLANGER_URLS' in self.config:
            if isinstance(self.config['FLANGER_URLS'], list):
                for urls in self.config['FLANGER_URLS']:
                    clz = extract_clz_from_string(urls)
                    for url, resource in clz.urls.items():
                        ep = f'{clz.__module__}.{clz.__name__}.{resource.__name__}'
                        self.add_url_rule(url, endpoint=ep)
                        self.endpoint_resource[ep] = resource()
            else:
                raise Exception('FLANGER_URLS must be list !!!')

    def init_request_processors(self):
        if 'FLANGER_REQUEST_PROCESSORS' in self.config:
            if not isinstance(self.config['FLANGER_REQUEST_PROCESSORS'], list):
                raise Exception('FLANGER_REQUEST_PROCESSORS must be list !!!')
            else:
                for processor in self.config['FLANGER_REQUEST_PROCESSORS']:
                    clz = extract_clz_from_string(processor)
                    self.request_processors.append(clz(self.endpoint_resource))

    def init_response_processors(self):
        if 'FLANGER_RESPONSE_PROCESSORS' in self.config:
            if not isinstance(self.config['FLANGER_RESPONSE_PROCESSORS'], list):
                raise Exception('FLANGER_RESPONSE_PROCESSORS must be list !!!')
            else:
                for processor in self.config['FLANGER_RESPONSE_PROCESSORS']:
                    clz = extract_clz_from_string(processor)
                    self.response_processors.append(clz)

    def bind_middleware(self):
        for processor in self.request_processors:
            pass
