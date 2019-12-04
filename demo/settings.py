import  os
import sys

# BASE_DIR =

FLANGER_URLS = [
    'api.v1.urls.V1Urls',
    'api.v2.urls.V2Urls',
]

FLANGER_MIDDLEWARES = ['flanger.restful.middleware.MiddleWareMin']