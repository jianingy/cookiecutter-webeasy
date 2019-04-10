from typing import List
import falcon
import warnings


_error_codes: List[int] = []


class _MetaException(type):

    def __new__(cls, name, bases, body):
        qualname = body['__qualname__']
        new_class = type.__new__(cls, name, bases, body)
        if new_class.error_code in _error_codes:
            warnings.warn(f'{qualname} has duplicated error_code',
                          stacklevel=2)
        else:
            _error_codes.append(new_class.error_code)
        return new_class


class GeneralException(Exception, metaclass=_MetaException):
    error_code = 1000
    error_format = 'an application exception occurred: %(reason)s'
    http_status_code = 500
    alert_sentry = True

    def __init__(self, message: str = None, data=None, alert=None, **kwargs):
        self.data = data
        self.kwargs = kwargs

        if alert is not None:
            self.alert_sentry = alert

        if not message:
            try:
                message = self.error_format % self.kwargs
            except KeyError:
                message = f'cannot format exception: {self.error_format}'

        self.message = message
        super().__init__(message)


class ClientException(GeneralException):
    error_format = '%(reason)s'
    error_code = 400000
    http_status_code = falcon.HTTP_400


class ServerException(GeneralException):
    error_format = '%(reason)s'
    error_code = 500000
    http_status_code = falcon.HTTP_500
