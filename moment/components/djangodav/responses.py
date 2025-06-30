try:
    import httplib
except ImportError:
    from http import client as httplib
from django.http import HttpResponse


# When possible, code returns an HTTPResponse sub-class. In some situations, we want to be able
# to raise an exception to control the response (error conditions within utility functions). In
# this case, we provide HttpError sub-classes for raising.


class ResponseException(Exception):
    """A base HTTP error class. This allows utility functions to raise an HTTP error so that
    when used inside a handler, the handler can simply call the utility and the correct
    HttpResponse will be issued to the client."""

    def __init__(self, response, *args, **kwargs):
        super(ResponseException, self).__init__('Response excepted', *args, **kwargs)
        self.response = response


class HttpResponsePreconditionFailed(HttpResponse):
    status_code = httplib.PRECONDITION_FAILED


class HttpResponseMediatypeNotSupported(HttpResponse):
    status_code = httplib.UNSUPPORTED_MEDIA_TYPE


class HttpResponseMultiStatus(HttpResponse):
    status_code = httplib.MULTI_STATUS


class HttpResponseNotImplemented(HttpResponse):
    status_code = httplib.NOT_IMPLEMENTED


class HttpResponseBadGateway(HttpResponse):
    status_code = httplib.BAD_GATEWAY


class HttpResponseCreated(HttpResponse):
    status_code = httplib.CREATED


class HttpResponseNoContent(HttpResponse):
    status_code = httplib.NO_CONTENT


class HttpResponseConflict(HttpResponse):
    status_code = httplib.CONFLICT


class HttpResponseLocked(HttpResponse):
    status_code = httplib.LOCKED


class HttpResponseUnAuthorized(HttpResponse):
    status_code = httplib.UNAUTHORIZED
