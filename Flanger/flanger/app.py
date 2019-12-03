from flask import Flask, request
from .restful.middleware import BaseMiddleWare
from .restful.urls import FlangerUrls
import importlib


class FlangerApp(Flask):
    endpoint_resource = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def init(self):
        self.bind_db()
        self.bind_urls()
        self.before_request(self.bind_middleware)

    def bind_urls(self):
        for url, resource in FlangerUrls.urls.items():
            self.add_url_rule(url, endpoint=resource.__name__)
            self.endpoint_resource[resource.__name__] = resource()
        if 'URLS' in self.config and isinstance(self.config['URLS'], list):
            for urls_module in self.config['URLS']:
                importlib.import_module(urls_module)
        for clz in FlangerUrls.__subclasses__():
            print(clz)

    def bind_db(self):
        pass

    def bind_middleware(self):
        BaseMiddleWare().process_request(request)
