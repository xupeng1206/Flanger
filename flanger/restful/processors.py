"""
作者         xupeng
邮箱         874582705@qq.com
github主页   https://github.com/xupeng1206

"""

from .response import FlangerResponse
from .exceptions import FlangerError, UrlNotFound, MethodNotImplement
from .resource import SwaggerResource
from .utils import extract_params
from flanger.keywords import *
from flask import send_file
import os
import logging

logger = logging.getLogger(__name__)


class BaseRequestProcessor:
    """
    BaseRequestProcessor: 框架层面的请求处理模块。

    用于处于请求，在这里它会请求的信息，找到对应的resource中的对应的方法，
    并将对应方法返回的dict和list处理成一个json-response返回出去

    self.app: 就是flanger的核心对象(flask核心对象+flanger自己的一些东西)

    process_request: 请求处理的逻辑部分
    """

    def __init__(self, app, *args, **kwargs):
        self.app = app

    def process_request(self, request, *args, **kwargs):
        try:
            # 获取url规则
            url_rule = request.url_rule
            if not url_rule:
                # url_rule为空的话, 证明path配置失败
                raise UrlNotFound

            # 通过url_rule获取对应endpoint,在用endpoint去endpoint_resource里面找对应的resource
            resource = self.app.endpoint_resource[url_rule.endpoint] if url_rule.endpoint in self.app.endpoint_resource else None
            if resource is None:
                raise UrlNotFound

            # 获取方法名（get? post? put? delete?）
            request_method = request.method.lower()
            method = getattr(resource, request_method, None)
            if method is None:
                raise MethodNotImplement

            # 将request也当成参数给到resource里面具体的算法
            params = {'request': request}
            # 抽取request中的一些参数，包括url传参，body传参等等
            ret_params = extract_params(request)
            if isinstance(ret_params, dict):
                # 更新params
                params.update(ret_params)

            # 执行相应方法的逻辑
            data = method(**params)

            # 成功 处理成json-response
            return FlangerResponse.success(data if not data is None else {})

        except FlangerError as e:
            # 自定义错误类型处理
            logger.error(e.msg)
            if self.app.config['DEBUG']:
                return FlangerResponse.error(e.code, e.msg)
            else:
                return FlangerResponse.error(e.code)
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

    def process_request(self, request, *args, **kwargs):
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
