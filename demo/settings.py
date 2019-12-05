import  os
import sys

# BASE_DIR =

FLANGER_URLS = [
    'api.v1.urls.V1Urls',
    'api.v2.urls.V2Urls',
]

FLANGER_REQUEST_PROCESSORS = [
    'api.v1.processors.ReqProcessor',
    'api.v2.processors.ReqProcessor',
]

FLANGER_RESPONSE_PROCESSORS = [
    'api.v1.processors.ResProcessor',
    'api.v2.processors.ResProcessor',
]