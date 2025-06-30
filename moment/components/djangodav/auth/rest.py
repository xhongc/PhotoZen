from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from djangodav.responses import HttpResponseUnAuthorized

try:
    import rest_framework
    from rest_framework.exceptions import APIException
except ImportError:
    rest_framework = None


class RequestWrapper(object):
    """ simulates django-rest-api request wrapper """
    def __init__(self, request):
        self._request = request
    def __getattr__(self, attr):
        return getattr(self._request, attr)
    
    
class RestAuthViewMixIn(object):
    authentications = NotImplemented

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        assert rest_framework is not None, "django rest framework is not installed."
        if request.method.lower() != 'options':
            user_auth_tuple = None
            for auth in self.authentications:
                try:
                    user_auth_tuple = auth.authenticate(RequestWrapper(request))
                except APIException as e:
                    return HttpResponse(e.detail, status=e.status_code)
                else:
                    if user_auth_tuple is None:
                        continue # try next authenticator 
                    else:
                        break    # we got auth, so stop trying

            if user_auth_tuple is not None:
                user, auth = user_auth_tuple
            else:
                resp = HttpResponseUnAuthorized("Not Authorised")
                resp['WWW-Authenticate'] = self.authentications[0].authenticate_header(request)
                return resp

            request.user = user
            request.auth = auth
        return super(RestAuthViewMixIn, self).dispatch(request, *args, **kwargs)
