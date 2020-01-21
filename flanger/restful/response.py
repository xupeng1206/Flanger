"""
作者         xupeng
邮箱         874582705@qq.com
github主页   https://github.com/xupeng1206

"""

from flask import jsonify
from .exceptions import FlangerError


class FlangerResponse:
    """
    response处理类，主要将正常返回值或exeception处理成json-response
    """

    @staticmethod
    def error(code, msg=''):
        """
        处理execution (processor内产生的，resource产生的)
        :param code:  错误代码
        :param msg:   错误信息
        :return: json-response
        """
        res = {
            'success': False,
            'code': code,
            'message': msg,
            'data': {}
        }
        return jsonify(res)

    @staticmethod
    def success(data):
        """
        处理正常返回值（支持dict和list）
        :param data:  返回的数据
        :return: json-response
        """
        if not isinstance(data, dict) or isinstance(data, list):
            raise TypeError(f'Reources Return Must Be Dict Or List !!!')

        return jsonify({
            'success': True,
            'code': 200,
            'message': '',
            'data': data
        })

    @staticmethod
    def raisee(e):
        """
        处理processor外部的execution
        外部返回FlangerError时，不用这个包一下的话，最终返回诶浏览器的可能是个常规的excption界面，
        而不是带错误信息的json-response，容易在开发中对接中出现一些麻烦
        :param e:
        :return:
        """
        if isinstance(e(), FlangerError):
            return FlangerResponse.error(e.code, e.msg)
        else:
            # 不是FlangerError类型的错误，只能原样抛出
            raise e
