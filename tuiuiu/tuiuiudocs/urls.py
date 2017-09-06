from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from tuiuiu.tuiuiudocs.views import serve

urlpatterns = [
    url(r'^(\d+)/(.*)$', serve.serve, name='tuiuiudocs_serve'),
    url(r'^authenticate_with_password/(\d+)/$', serve.authenticate_with_password,
        name='tuiuiudocs_authenticate_with_password'),
]
