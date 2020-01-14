"""
作者         xupeng
邮箱         874582705@qq.com
github主页   https://github.com/xupeng1206

"""

from flask import jsonify


class FlangerResponse:

    @staticmethod
    def error(code, msg=''):
        res = {
            'success': False,
            'code': code,
            'message': msg,
            'data': {}
        }
        return jsonify(res)

    @staticmethod
    def success(data):
        if not isinstance(data, dict) or isinstance(data, list):
            raise TypeError(f'Reources Return Must Be Dict Or List !!!')

        return jsonify({
            'success': True,
            'code': 200,
            'message': '',
            'data': data
        })
