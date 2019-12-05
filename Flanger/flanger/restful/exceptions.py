class FlangerError(Exception):
    code = 1000
    msg = 'Server Inner Error !!!'


class UrlNotFound(FlangerError):
    code = 1001
    msg = 'Url Not Found !!!'


class MethodNotImplement(FlangerError):
    code = 1002
    msg = 'Api Not Implement !!!'

