"""
作者         xupeng
邮箱         874582705@qq.com / 15601598009@163.com
github主页   https://github.com/xupeng1206

"""

from flask import Flask, request
from .restful.processors import BaseRequestProcessor, BaseResponseProcessor, FlangerStaticProcessor, \
    FlangerSwaggerProcessor
from .restful.utils import extract_clz_from_string
from .restful.swagger import generate_swagger_json
from .restful.exceptions import UrlNotFound
from .restful.response import FlangerResponse
from .keywords import *
import logging

logger = logging.getLogger(__name__)


class FlangerApp(Flask):
    """
    Flanger 核心类

    继承于Flask 添加一些新的属性

    """
    endpoint_resource = {}                # endpoint为key, resource对象为value的dict, 记录所有注册的resource
    endpoint_url = {}                     # endpoint为key, url为value的dict, 配合endpoint_resource使用
    request_processors = []               # 记录所有自定义的request  processor, 顺序同app的settings中配置的一样
    response_processors = []              # 记录所有自定义的response processor, 顺序同app的settings中配置的一样
    flanger_static_processor = None       # swagger用到的静态资源的processor
    flanger_swagger_processor = None      # swagger_resource对应的processor

    def __init__(self, *args, **kwargs):
        """
        实例化, 调用父类Flask的实例化过程

        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)

    def init(self):
        """
        Flanger 相关功能的init, 这一函数在实例化Flanger核心对象必须执行，不然Flanger的相关功能，没办法使用

        :return:
        """
        # 根据setting中urls配置，注册url及关联相对应resource
        self.init_urls()

        # init_urls后初始化swagger相关的内容，包括swagger的url, swagger静态资源的绑定
        self.init_swagger()

        # 根据settings中processor设置 初始化 request_processors和response_processors
        self.init_request_processors()
        self.init_response_processors()

        # 调用flask的before_request，让请求进入flask的视图函数前，先进行bind_processor中的逻辑
        # 在bind_processor中直接返回一个response, 让其不再进入后续的视图函数环节，直接return出去
        # 这样只要在bind_processor 重新构建一个请求进来，到一个response出去的过程就行
        self.before_request(self.bind_processor)

    def init_urls(self):
        """
        初始化url，resources相关的信息

        :return:
        """

        # app的settings（config）中必须要有FLANGER_URLS的配置，且是list
        # 所以有一点要求，实例化Flanger后，必须先加载settings, (app.config.from_object等方法)，再app.init()
        if FLANGER_URLS in self.config:
            if isinstance(self.config[FLANGER_URLS], list):
                for urls in self.config[FLANGER_URLS]:
                    # 获取settings中指定到的那些类对象  （必须符合url类对象的格式）
                    clz = extract_clz_from_string(urls)

                    # 判断是否有统一的url前缀
                    prefix = ''
                    if hasattr(clz, URL_PREFIX):
                        url_prefix = getattr(clz, URL_PREFIX)
                        prefix = f'/{url_prefix.strip("/")}'

                    # 遍历url中的条目，添加对应关系到endpoint_resource, endpoint_url, 并调用flask的add_url_rule进行注册
                    for url, resource in clz.urls.items():
                        url = f'{prefix}/{url.strip("/")}'
                        # 产生allowed_methods
                        allowed = []
                        for method in ['get', 'post', 'put', 'delete']:
                            if hasattr(resource, method):
                                allowed.append(method)
                        resource.allowed_methods = allowed
                        ep = f'{clz.__module__}.{clz.__name__}.{resource.__name__}'
                        self.add_url_rule(url, endpoint=ep, methods=['GET', 'POST', 'PUT', 'DELETE'])
                        self.endpoint_resource[ep] = resource()
                        self.endpoint_url[ep] = url
            else:
                raise Exception(f'{FLANGER_URLS} must be list !!!')

    def init_swagger(self):
        """
        出事话swagger相关
        :return:
        """
        # 注册/swagger 访问 swagger_index.html
        self.add_url_rule('/swagger', endpoint='swagger')
        # 注册swagger_index.html 中所用静态文件的url
        self.add_url_rule('/fstatic/<filepath>', endpoint='fstatic', methods=['GET'])
        # 注册/favicon.ico 不管也没事，但是后台常报找不到favicon.ico的错误，很烦，这里处理一下子，让后台干净一点
        self.add_url_rule('/favicon.ico', endpoint='favicon')

        # 实例化swagger processor 和 swagger 静态文件的processor
        self.flanger_swagger_processor = FlangerSwaggerProcessor(self)
        self.flanger_static_processor = FlangerStaticProcessor(self)

        # 生成swagger.json时是放在app的目录下的某个位置的 所以BASE_DIR必须要有
        if BASE_DIR not in self.config:
            raise Exception(f'{BASE_DIR} must in settings !!!')

        # 生成对应的swagger.json
        generate_swagger_json(self)

    def init_request_processors(self):
        """
        初始化 request processors

        :return:
        """
        if FLANGER_REQUEST_PROCESSORS in self.config:
            if not isinstance(self.config[FLANGER_REQUEST_PROCESSORS], list):
                raise Exception(f'{FLANGER_REQUEST_PROCESSORS} must be list !!!')
            else:
                for processor in self.config[FLANGER_REQUEST_PROCESSORS]:
                    clz = extract_clz_from_string(processor)

                    # 如果自定义processors 继承于BaseRequestProcessor，直接放进request_processors就行
                    if clz in BaseRequestProcessor.__subclasses__():
                        self.request_processors.append(clz(self))
                    else:
                        # 如果没有继承BaseRequestProcessor，给它补上 __init__,再放入request_processors
                        # 让他在process_request时顺利使用核心对象app
                        def __init__(self, app, *args, **kwargs):
                            self.app = app

                        clz.__init__ = __init__

                        self.request_processors.append(clz(self))

    def init_response_processors(self):
        """
        初始化 response processors

        :return:
        """
        if FLANGER_RESPONSE_PROCESSORS in self.config:
            if not isinstance(self.config[FLANGER_RESPONSE_PROCESSORS], list):
                raise Exception(f'{FLANGER_RESPONSE_PROCESSORS} must be list !!!')
            else:
                for processor in self.config[FLANGER_RESPONSE_PROCESSORS]:
                    clz = extract_clz_from_string(processor)

                    # 如果自定义processors 继承于BaseRequestProcessor，直接放进response_processors就行
                    if clz in BaseResponseProcessor.__subclasses__():
                        self.response_processors.append(clz(self))
                    else:
                        # 如果没有继承BaseResponseProcessor，给它补上 __init__,再放入response_processors
                        # 让他在process_response时顺利使用核心对象app
                        def __init__(self, app, *args, **kwargs):
                            self.app = app

                        clz.__init__ = __init__
                        self.response_processors.append(clz(self))

    def bind_processor(self):
        """
        bind_processor, 在request进视图函数前，拦截下来，做我们框架自己的逻辑
        :return:
        """

        # swagger 静态文件 等  start
        # 为了让BaseRequestProcessor尽量干净点，加swagger和静态文件的处理，移到了这里
        # 这样也方便自定义request processor, 尽量避免因自定义request processor时考虑不全，让原本的swagger及静态文件的功能报废
        url_rule = request.url_rule
        if not url_rule:
            # url未注册，url not found
            return FlangerResponse.raisee(UrlNotFound)

        # 处理访问swagger页面时
        if url_rule.endpoint.strip('/') == 'swagger':
            return self.flanger_swagger_processor.process_request(request)

        # 处理flanger 自身的swagger的static
        if url_rule.endpoint.strip('/') in ['fstatic', 'favicon']:
            return self.flanger_static_processor.process_request(request)

        # 静态文件不走flanger逻辑，走flask原本的逻辑 (app自己用的静态文件）
        # static_url 不能是fstatic, fstatic会被理解成flanger swagger_index.html所需静态文件的
        if url_rule.endpoint.strip('/') == self.static_url_path.strip('/'):
            return
        # swagger 静态文件 等  end

        # 按照request processors的顺序，逐一处理
        for processor in self.request_processors:
            if hasattr(processor, 'process_request'):
                response = processor.process_request(request)
                if response:
                    return response

        # 进入框架默认的request processor
        response = BaseRequestProcessor(self).process_request(request)

        # 按照response processors的顺序， 逐一处理response
        # 不管怎么样 这里要return 出来一个response
        for processor in self.response_processors:
            if hasattr(processor, 'process_response'):
                response = processor.process_response(response)

        # bind_processor 这个函数，在最后返回一个response的话，response就会直接出去，返回给浏览器
        # 若果这里没有return一个response的话，请求就进入去找视图函数，但是app这时候只有resource，和原本flask的视图函数形式不一样
        # 结果不可预期， 开发自定义processor的时候，一定要注意
        return response
