from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from djangodav.responses import HttpResponseUnAuthorized


class TastypieAuthViewMixIn(object):
    authentication = NotImplemented

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):

        if request.method.lower() != 'options':
            auth_result = self.authentication.is_authenticated(request)

            if isinstance(auth_result, HttpResponse):
                return auth_result

            if auth_result is not True:
                return HttpResponseUnAuthorized()

        return super(TastypieAuthViewMixIn, self).dispatch(request, *args, **kwargs)
