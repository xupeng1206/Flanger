from flanger.restful.urls import FlangerUrls
from .resource import HelloResource

class V2Urls(FlangerUrls):
    urls = {
        '/': HelloResource,
        '/hello/<abc>': HelloResource
    }


__all__ = ['V2Urls']