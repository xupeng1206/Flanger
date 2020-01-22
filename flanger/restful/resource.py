"""
作者         xupeng
邮箱         874582705@qq.com / 15601598009@163.com
github主页   https://github.com/xupeng1206

"""

from .exceptions import MethodNotImplement, UrlNotFound
from flask import send_file
import os


class SmartResource:
    """
    用当做基础的resource, 目前暂无用处。
    """

    def get(self, request, *args, **kwargs):
        """
        get api
        :param args:
        :param kwargs:
        :return:
        """
        raise MethodNotImplement

    def post(self, request,  *args, **kwargs):
        """
        post api
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        raise MethodNotImplement

    def put(self, request, *args, **kwargs):
        """
        put api
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        raise MethodNotImplement

    def delete(self, request, *args, **kwargs):
        """
        delete api
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        raise MethodNotImplement


class SwaggerResource:
    """
    swagger对应的resource，主要用来返回swagger_index.html

    """

    def get(self, debug, *args, **kwargs):
        """
        get方法 返回swagger_index.html
        :param debug:
        :param args:
        :param kwargs:
        :return:
        """
        if debug:
            # debug模式下展现swagger界面
            import flanger
            return send_file(os.path.join(flanger.__swagger__, 'swagger_index.html'))
        else:
            # 生产模式下 不提供swagger
            raise UrlNotFound
