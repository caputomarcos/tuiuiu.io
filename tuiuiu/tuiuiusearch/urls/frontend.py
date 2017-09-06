from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from tuiuiu.tuiuiusearch.views import search

urlpatterns = [
    url(r'^$', search, name='tuiuiusearch_search'),
    url(r'^suggest/$', search, {'use_json': True}, name='tuiuiusearch_suggest'),
]
