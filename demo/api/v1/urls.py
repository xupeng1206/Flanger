from .resource import HelloResource
from flanger.restful.urls import FlangerUrls


class V1Urls(FlangerUrls):
    urls = {
        '/hello': HelloResource
    }


__all__ = ['V1Urls']
