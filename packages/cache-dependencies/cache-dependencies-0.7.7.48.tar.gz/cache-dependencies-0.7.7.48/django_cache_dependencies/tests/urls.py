from __future__ import absolute_import, unicode_literals
from django.conf.urls import url
from django_cache_dependencies.decorators import cache_page
from django_cache_dependencies.tests import views


urlpatterns = [
    url(r"^cache_tagging_test_decorator/$",
        views.test_decorator,
        name="cache_tagging_test_decorator"),
    url(r"^cache_tagging_test_decorator_cbv1/$",
        views.TestDecoratorView1.as_view(),
        name="cache_tagging_test_decorator_cbv1"),
    url(r"^cache_tagging_test_decorator_cbv2/$",
        cache_page(3600, tags=lambda request: ('tests.firsttestmodel', ))(views.TestDecoratorView2.as_view()),
        name="cache_tagging_test_decorator_cbv2"),
    url(r"^cache_tagging_test_decorator_cbv3/$",
        views.TestDecoratorView3.as_view(),
        name="cache_tagging_test_decorator_cbv3"),
    url(r"^cache_tagging_test_decorator_cbv4/$",
        views.TestDecoratorView4.as_view(),
        name="cache_tagging_test_decorator_cbv4"),
]
