from flask import jsonify


class FlangerResponse:

    @staticmethod
    def error(code, msg=''):
        res = {
            'ok': False,
            'code': code,
            'msg': msg,
            'data': {}
        }
        return jsonify(res)

    @staticmethod
    def success(data):
        if isinstance(data, dict) or isinstance(data, list):
            raise TypeError(f'Reources Return Must Be Dict Or List !!!')

        return jsonify({
            'ok': True,
            'code': 200,
            'msg': '',
            'data': data
        })
