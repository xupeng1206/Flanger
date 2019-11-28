from flask import Flask, request, session, g, current_app
from .restful.middleware import BaseAppMiddleWare

# 单例
def create_app(f_name):

    app = Flask(f_name)
    
    # 钩子函数 before_first_request
    @app.before_first_request
    def before_first_request():
        BaseAppMiddleWare().before_first_request(request, session, g, current_app)

    # 钩子函数 before_request
    @app.before_request
    def before_request():
        BaseAppMiddleWare().before_request(request, session, g, current_app)

    # 钩子函数 after_request
    @app.after_request
    def after_request(response):
        return BaseAppMiddleWare().after_request(response)

    # 钩子函数 teardown_request
    @app.teardown_request
    def teardown_request(e):
        return BaseAppMiddleWare().teardown_request(e)

    return app
