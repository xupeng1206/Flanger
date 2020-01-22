"""
作者         xupeng
邮箱         874582705@qq.com / 15601598009@163.com
github主页   https://github.com/xupeng1206

"""


class FlangerError(Exception):
    """
    Flanger中错误类型的基类，只要继承于它的错误类型，都可以被process捕捉，统一处理成json response形式返回

    attr1: code  错误代码 Flanger内部，目前用了1000,1001,1002, 若在app中通过继承该类自定义错误，建议从2000开始
    attr2: msg   错误消息
    """
    code = 1000
    msg = 'Server Inner Error !!!'


class UrlNotFound(FlangerError):
    """
    url配置失败，url找不到的错误
    """
    code = 1001
    msg = 'Url Not Found !!!'


class MethodNotImplement(FlangerError):
    """
    方法没有实现的错误
    """
    code = 1002
    msg = 'Api Not Implement !!!'

