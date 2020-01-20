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

    用于处于请求(类似django的middleware处理request的那部分内容)，在这里它会请求的信息，找到对应的resource中的对应的方法，
    并将对应方法返回的dict和list处理成一个json-response返回出去。
    同样它也作为自定义request processor的基类，必须继承与它，自定义基类才有效


    self.app: 就是flanger的核心对象(flask核心对象+flanger自己的一些东西)

    process_request: 请求处理的逻辑部分
    """

    def __init__(self, app, *args, **kwargs):
        """

        :param app: 就是flanger的核心对象(flask核心对象+flanger自己的一些东西)
        :param args:
        :param kwargs:
        """
        self.app = app

    def process_request(self, request, *args, **kwargs):
        """
        process_request
        :param request:
        :param args:
        :param kwargs:
        :return: response
        """
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
    """
    BaseResponseProcessor: 框架层面的response处理模块。

    用于处于response(类似django的middleware处理response的那部分内容), 默认不做啥处理，直接返回
    写在这里，留一个可能性，也作为自定义response processor的基类，必须继承与它，自定义基类才有效

    self.app: 就是flanger的核心对象(flask核心对象+flanger自己的一些东西)

    process_response: 请求responnse的逻辑部分, 默认框架内啥都没做
    """

    def __init__(self, app, *args, **kwargs):
        """

        :param app: 就是flanger的核心对象(flask核心对象+flanger自己的一些东西)
        :param args:
        :param kwargs:
        """
        self.app = app

    def process_response(self, response):
        """
        请求responnse的逻辑部分
        :param response:
        :return: response
        """
        return response


class FlangerSwaggerProcessor:
    """
    专门用来处理swagger相关的processor

    开发人员想要访问swagger的时候，请求会走到这里，然后去找到swagger对应的resource中的get方法并执行
    这里swagger的resource和普通的resource有点不一样，这里swagger resource中的get方法返回是一个httpresponse, 而不是字典或list
    所以拿到返回值后直接返回就行了。

    self.app: 就是flanger的核心对象(flask核心对象+flanger自己的一些东西)

    process_request: 请求处理的逻辑部分
    """

    def __init__(self, app, *args, **kwargs):
        """

        :param app: 就是flanger的核心对象(flask核心对象+flanger自己的一些东西)
        :param args:
        :param kwargs:
        """
        self.app = app

    def process_request(self, request, *args, **kwargs):
        """
        process_request  (swagger )
        :param request:
        :param args:
        :param kwargs:
        :return: http response
        """
        try:
            url_rule = request.url_rule
            if not url_rule:
                raise UrlNotFound

            # 在进processor之前，就已经判断过endpoint了, 这里不是重付不必要的操作，直接实例化一个SwaggerResource
            resource = SwaggerResource()

            # 判断一些method, 正常使用的情况下都是get方法，用postman这些工具强行请求post之类的，直接抛一个MethodNotImplement就行
            request_method = request.method.lower()
            method = getattr(resource, request_method, None)
            if method is None:
                raise MethodNotImplement

            # 抽取参数
            params = {'request': request, 'debug': self.app.config['DEBUG']}
            ret_params = extract_params(request)
            if isinstance(ret_params, dict):
                params.update(ret_params)

            # 执行SwaggerResource的get方法，内部是个send_file，会得到一个http response，拿到后直接return
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
