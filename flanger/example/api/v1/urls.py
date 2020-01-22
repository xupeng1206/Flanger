"""
作者         xupeng
邮箱         874582705@qq.com / 15601598009@163.com
github主页   https://github.com/xupeng1206

"""

from .resource import HelloResource


class V1Urls:
    """
    类名随便取都行

    属性：
    1. url_prefix (可以没有)
        url的前缀，给这个类底下涉及的url都套上前缀, 如下面的 /hello会被注册成  /api/v1/hello, 若果没有url_prefix属性, /hello 会被注册成 /hello

    2. urls (必要属性，类型是dict)
        key:    url路径（flask中注册路径怎么写，这里就怎么写,如：/hello, /hello/<name> 等）
        value:  url对应的resource

        注：    这写url和resource对应关系时候，不用关心method和endpoint, 交由框架去处理

    重点：
        要想这个类有小，一定要在settings的FLANGER_URLS中注册
    """

    # url_prefix 属性可以没有
    url_prefix = '/api/v1'

    # urls属性必须要有
    urls = {
        # key: url, value: resource
        '/hello': HelloResource,
        # 可以在下面添加自己的url及对应的resource
        # ...

    }
