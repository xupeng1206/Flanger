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


__all__ = ['Singleton']