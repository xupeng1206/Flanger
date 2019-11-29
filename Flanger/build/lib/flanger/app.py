from flask import Flask, request
from .restful.middleware import BaseAppMiddleWare


class FlangerApp(Flask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind_db()
        self.before_request(self.bind_middleware)

    def bind_db(self):
        pass

    def bind_middleware(self):
        BaseAppMiddleWare().process_request(request)
