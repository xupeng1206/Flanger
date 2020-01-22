"""
作者         xupeng
邮箱         874582705@qq.com / 15601598009@163.com
github主页   https://github.com/xupeng1206

"""

import os

# 项目根目录（必填）
BASE_DIR = os.path.dirname(__file__)


# URL配置
# 使用列表中的指定的类注册路由
FLANGER_URLS = [
    'api.v1.urls.V1Urls',
    # 'api.v2.urls.V2Urls', ex
]


# # processor相关
# # request processor 配置写法和url的类似
# # 功能有点类似django的middlewave中处理request的部分
# FLANGER_REQUEST_PROCESSORS = []

# # response processor 配置写法和url的类似
# # 功能有点类似django的middlewave中处理response的部分
# FLANGER_RESPONSE_PROCESSORS = []


# sagger相关
# 自动swagger需要忽略的参数列表，比如token之类的
# SWAGGER_IGNORE_PARAMS = []
