from .resource import SwaggerResource


class FlangerUrls:
    urls = {
        '/swagger': SwaggerResource
    }
    # # 权重大于 regular_urls
    # # 单纯的url 例如 http://127.0.0.1:8000/hello?a=1&b=2
    # pure_urls = {
    #     '/swagger': SwaggerResource()
    # }
    #
    # # http://127.0.0.1:8000/hello/<param>/world
    # # 参数在url中， url正则匹配
    # regular_urls = {
    # }