from django import test
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from throttle.decorators import throttle
from throttle.views import ThrottleMixin


class ThrottleTest(test.TestCase):
    """
    Throttle decorator test suite
    """
    urls = 'throttle.tests'
    name_map = {
        'default': 'test_default',
        'method': 'test_method',
        'duration': 'test_duration',
        'response': 'test_response',
        'response_callable': 'test_response_callable',
    }

    def request(self, url, method='post', **kwargs):
        """
        The helper function that emulates HTTP request to
        Django views with given method
        """
        url = reverse(url)
        method = method.lower()
        return getattr(test.Client(), method)(url, **kwargs)

    def test_default(self):
        """
        Tests default usage
        """
        self.assertEquals(200, self.request(self.name_map['default']).status_code)
        self.assertEquals(403, self.request(self.name_map['default']).status_code)

    def test_method(self):
        """
        Tests that decorator applies to view for specified method and
        not applies for another
        """
        self.assertEquals(200, self.request(self.name_map['method'], method='GET').status_code)
        self.assertEquals(403, self.request(self.name_map['method'], method='GET').status_code)
        self.assertEquals(200, self.request(self.name_map['method'], method='POST').status_code)

    def test_response(self):
        """
        Tests custom response decorator argument
        """
        good = self.request(self.name_map['response'])
        bad = self.request(self.name_map['response'])
        self.assertEquals(200, good.status_code)
        self.assertEquals(401, bad.status_code)
        self.assertContains(text='Response', response=bad, status_code=401)

    def test_response_callable(self):
        """
        Tests custom response decorator argument
        """
        self.assertEquals(200, self.request(self.name_map['response_callable']).status_code)
        self.assertEquals(401, self.request(self.name_map['response_callable']).status_code)
        self.assertContains(text='Request Response', response=self.request(self.name_map['response_callable']), status_code=401)

    def test_duration(self):
        """
        Tests custom duration
        """
        self.assertEquals(200, self.request(self.name_map['duration']).status_code)
        self.assertEquals(200, self.request(self.name_map['duration']).status_code)


def index(request):
    """
    Test view function
    """
    return HttpResponse("Test view")


urlpatterns = [
    url(r'^$', throttle(index), name='test_default'),
    url(r'^method/$', throttle(index, method='GET'), name='test_method'),
    url(r'^duration/$', throttle(index, duration=0), name='test_duration'),
    url(r'^response/$', throttle(index, response=HttpResponse('Response', status=401)), name='test_response'),
    url(r'^response/callable/$', throttle(index, response=lambda request: HttpResponse('Request Response', status=401)), name='test_response_callable'),
]


try:
    from django.views.generic import View
except ImportError as e:
    pass
else:
    class IndexView(ThrottleMixin, View):
        """
        Class based view for mixin test
        """
        def get(self, request):
            return index(request)

        def post(self, request):
            return self.get(request)

    urlpatterns += [
        url(r'^cbv/$', IndexView.as_view(), name='test_cbv_default'),
        url(r'^cbv/method/$', IndexView.as_view(method='GET'), name='test_cbv_method'),
        url(r'^cbv/duration/$', IndexView.as_view(duration=0), name='test_cbv_duration'),
        url(r'^cbv/response/$', IndexView.as_view(response=HttpResponse('Response', status=401)), name='test_cbv_response'),
        url(r'^cbv/response/callable/$', IndexView.as_view(response=lambda request: HttpResponse('Request Response', status=401)), name='test_cbv_response_callable'),
    ]

    class ThrottleMixinTest(ThrottleTest):
        """
        ThrottleMixin test suite
        """
        name_map = {
            'default': 'test_cbv_default',
            'method': 'test_cbv_method',
            'duration': 'test_cbv_duration',
            'response': 'test_cbv_response',
            'response_callable': 'test_cbv_response_callable',
        }
