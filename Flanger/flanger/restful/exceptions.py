"""
作者         xupeng
邮箱         874582705@qq.com
github主页   https://github.com/xupeng1206

"""


class FlangerError(Exception):
    code = 1000
    msg = 'Server Inner Error !!!'


class UrlNotFound(FlangerError):
    code = 1001
    msg = 'Url Not Found !!!'


class MethodNotImplement(FlangerError):
    code = 1002
    msg = 'Api Not Implement !!!'

