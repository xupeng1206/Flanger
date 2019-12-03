from .urls import FlangerUrls
from .utils import Singleton
from .response import FlangerResponse
import re
import logging

logger = logging.getLogger(__name__)


@Singleton
class BaseMiddleWare:

    endpoint_resource = {}

    def process_request(self, request, *args, **kwargs):
        url_rule = request.url_rule
        if not url_rule:
            error_msg = f'{url_rule.string} Not Found!!!'
            logging.info(error_msg)
            return FlangerResponse.error(404, error_msg)
        try:
            resource = self.endpoint_resource[url_rule.endpoint]
        except Exception as e:
            return

