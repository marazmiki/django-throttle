from django.core.cache import cache
from django.http import HttpResponseForbidden, HttpResponse


class ThrottleMixin(object):
    duration = 15
    method = 'POST'
    response = None

    def remote_addr(self):
        return self.request.META.get('HTTP_X_FORWARDED_FOR') or self.request.META.get('REMOTE_ADDR')

    def cache_key(self):
        return '{addr}.{path}'.format(addr=self.remote_addr(), 
            path=self.request.get_full_path())

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs

        if (self.response and not isinstance(self.response, HttpResponse)
            and not callable(self.response)):
            raise TypeError("The `response` keyword argument must "
                            "be a either HttpResponse instance or "
                            "callable with `request` argument")

        if self.request.method == self.method:
            key = self.cache_key()

            if cache.get(key):
                if callable(self.response):
                    return self.response(request)

                elif self.response:
                    return self.response

                else:
                    return HttpResponseForbidden('Try slowing down a little.')

            cache.set(key, 1, self.duration)

        return super(ThrottleMixin, self).dispatch(request, *args, **kwargs)


def throttle(func, method='POST', duration=15, response=None):
    """
    This decorator is based on Django snippet #1573 code that 
    can be found at http://djangosnippets.org/snippets/1573/

    Simple usage

        @throttle
        def my_view(request):
            ""

    You can specify each of HTTP method

        @throttle(method='GET')
        def my_get_view(request)
            ""

    Custom

    """
    if response:
        if not isinstance(response, HttpResponse) and  not callable(response):
            raise TypeError, "The `response` keyword argument must " + \
                             "be a either HttpResponse instance or " + \
                             "callable with `request` argument.    "

    def inner(request, *args, **kwargs):
        if request.method == method:
            remote_addr = request.META.get('HTTP_X_FORWARDED_FOR') or \
                          request.META.get('REMOTE_ADDR')

            key = '{addr}.{path}'.format(addr=remote_addr, 
                                         path=request.get_full_path())
            if cache.get(key):
                if callable(response):
                    return response(request)

                elif response:
                    return response

                else:
                    return HttpResponseForbidden('Try slowing down a little.')

            cache.set(key, 1, duration)
        return func(request, *args, **kwargs)
    return inner
