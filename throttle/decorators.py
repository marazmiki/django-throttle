from django.core.cache import cache
from django.http import HttpResponseForbidden, HttpResponse

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
