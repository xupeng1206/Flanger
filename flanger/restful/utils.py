"""
作者         xupeng
邮箱         874582705@qq.com
github主页   https://github.com/xupeng1206

"""

import threading
import importlib
import json
from json.decoder import JSONDecodeError
import traceback

import logging

logger = logging.getLogger(__name__)


def lock(func):
    func.__lock__ = threading.Lock()

    def wrapper(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)

    return wrapper


def Singleton(cls):
    __instances = {}

    @lock
    def wrapper(*args, **kw):
        if cls not in __instances:
            __instances[cls] = cls(*args, **kw)
        return __instances[cls]

    return wrapper


def extract_clz_from_string(module_str):
    file_module_str = '.'.join(module_str.split('.')[:-1])
    clz_str = module_str.split('.')[-1]
    module = importlib.import_module(file_module_str)
    clz = getattr(module, clz_str, None)
    if clz is None:
        raise Exception(f'{module_str} class not Found !!!')
    return clz


def guess_val(val):
    """
        10.0    --> 10
        10.1    --> 10.1
        10      --> 10
        'abc'   --> 'abc'
        '10.0'  --> 10
        '10.1'  --> 10.1
        '10'    --> 10
    """
    if not isinstance(val, str) or isinstance(val, int) or isinstance(val, float):
        return val
    try:
        try:
            if float(val) == int(val):
                return int(val)
            raise Exception
        except Exception as e:
            if '.' in val:
                return float(val)
            else:
                return int(val)
    except Exception as e:
        if val == 'false':
            return False
        if val == 'true':
            return True
        return val


def extract_params(request):
    params = {}
    # params in re style in url like  /hello/<name>  name: xxx
    if request.view_args:
        for k, v in request.view_args.items():
            params[k.lower()] = guess_val(v)

    # params at the right of the question mark  /hello/<name>?abc=123  abc: 123
    if request.args:
        for k, v in request.args.items():
            params[k.lower()] = guess_val(v)

    # data
    if request.data:
        try:
            data_str = str(request.data, encoding='utf-8').replace('\n', '').replace('\r', '').replace('\t', '')
            if data_str:
                data_json = json.loads(data_str)
                for k, v in data_json.items():
                    params[k.lower()] = guess_val(v)
        except JSONDecodeError as e:
            logger.warning(traceback.format_exc())
        except Exception as e:
            logger.debug(traceback.format_exc())

    if request.json:
        for k, v in request.json.items():
            params[k.lower()] = guess_val(v)

    # form-data
    if request.form:
        for k, v in request.form.items():
            params[k.lower()] = guess_val(v)

    # files
    if request.files:
        for k, v in request.form.items():
            params[k.lower()] = guess_val(v)

    return params
