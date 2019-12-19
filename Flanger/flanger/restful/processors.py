from .response import FlangerResponse
from .exceptions import FlangerError, UrlNotFound, MethodNotImplement
from .utils import extract_params
import logging

logger = logging.getLogger(__name__)


class BaseRequestProcessor:

    endpoint_resource = {}

    def __init__(self, resources, *args, **kwargs):
        self.endpoint_resource = resources

    def process_request(self, request, *args, **kwargs):
        try:
            url_rule = request.url_rule
            if not url_rule:
                raise UrlNotFound

            resource = self.endpoint_resource[url_rule.endpoint] if url_rule.endpoint in self.endpoint_resource else None
            if resource is None:
                raise UrlNotFound

            request_method = request.method.lower()
            method = getattr(resource, request_method, None)
            if method is None:
                raise MethodNotImplement

            params = {'request': request}
            ret_params = extract_params(request)
            if isinstance(ret_params, dict):
                params.update(ret_params)

            data = method(**params)
            return FlangerResponse.success(data if not data is None else {})

        except FlangerError as e:
            logger.error(e.msg)
            return FlangerResponse.error(e.code, e.msg)
        except Exception as e:
            raise e


class BaseResponseProcessor:

    def process_response(self, response):
        return response