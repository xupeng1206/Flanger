import threading
import importlib


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


def extract_clz_from_string(module_str):
    file_module_str = '.'.join(module_str.split('.')[:-1])
    clz_str = module_str.split('.')[-1]
    module = module_str.import_module(file_module_str)
    clz = getattr(module, clz_str, None)
    if clz is None:
        raise Exception(f'{module_str} class not Found !!!')
    return clz


__all__ = ['Singleton', 'extract_clz_from_string']
