from .urls import FlangerUrls
import threading


def lock(func):
    func.__lock__ = threading.Lock()

    def wrapper(*args, **kwargs):
        with func.__lock__:
            return func(*args, **kwargs)

    return wrapper


def Singleton(cls):
    __instances = {}

    @lock
    def wrapper(*args, **kw):
        if cls not in __instances:
            __instances[cls] = cls(*args, **kw)
        return __instances[cls]

    return wrapper


class BaseMiddleWare:

    def __init__(self, *args, **kwargs):
        self.pure_urls = FlangerUrls.pure_urls
        self.regular_urls = FlangerUrls.pure_urls

        for sub_clz in FlangerUrls.__subclasses__():
            self.pure_urls.update(sub_clz().pure_urls)
            self.regular_urls.update(sub_clz().regular_urls)

    def process_request(self, request, *args, **kwargs):
        a = 1
        pass
