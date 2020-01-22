"""
作者         xupeng
邮箱         874582705@qq.com / 15601598009@163.com
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
    """
    线程锁的装饰器
    :param func:
    :return:
    """
    func.__lock__ = threading.Lock()

    def wrapper(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)

    return wrapper


def Singleton(cls):
    """
    线程安全的单例装饰器
    :param cls:
    :return:
    """
    __instances = {}

    @lock
    def wrapper(*args, **kw):
        if cls not in __instances:
            __instances[cls] = cls(*args, **kw)
        return __instances[cls]

    return wrapper


def extract_clz_from_string(module_str):
    """
    从字符串模块名中抽出对应的python对象

    :param module_str:  例如  ‘example.api.v1.urls.V1Urls’
    :return:  class     例如   V1Urls （python对象）
    """
    file_module_str = '.'.join(module_str.split('.')[:-1])
    clz_str = module_str.split('.')[-1]
    module = importlib.import_module(file_module_str)
    clz = getattr(module, clz_str, None)
    if clz is None:
        raise Exception(f'{module_str} class not Found !!!')
    return clz


def guess_val(val):
    """
    标准话value值，参考下面例子
    :param val:
    :return:  val (formated)

    ex：

    666.0   -->  666
    66.6    -->  66.6
    666     -->  666
    'xxx'   -->  'xxx'
    '666.0' -->  666
    '66.1'  -->  66.6
    '60'    -->  60

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
    """
    解析request, 抽出当中的参数，并将他们组织成dict
    注意多种参数类型之间会有覆盖，开发时请注意
    在resource中想要原始的各部分的原值，仍然可以从request中获得

    :param request:
    :return: {}
    """
    params = {}
    # 1. params in re style in url like  /hello/<name>  name: xxx
    if request.view_args:
        for k, v in request.view_args.items():
            params[k.lower()] = guess_val(v)

    # 2. params at the right of the question mark  /hello/<name>?abc=123  abc: 123
    if request.args:
        for k, v in request.args.items():
            params[k.lower()] = guess_val(v)

    # request.json 只能够接受方法为POST、Body为raw，raw类型为json 即header内容为application/json的数据
    # request.dada 能够同时接受方法为POST、Body为raw, raw类型为text或json的数据
    # 3. data
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

    # 4. json
    if request.json:
        for k, v in request.json.items():
            params[k.lower()] = guess_val(v)

    # 5. form-data
    if request.form:
        for k, v in request.form.items():
            params[k.lower()] = guess_val(v)

    # 6. files
    if request.files:
        for k, v in request.form.items():
            params[k.lower()] = guess_val(v)

    return params
