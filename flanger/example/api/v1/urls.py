from .resource import HelloResource


class V1Urls:
    url_prefix = '/api/v1'
    urls = {
        '/hello': HelloResource
    }
