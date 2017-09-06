from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import views as auth_views

from tuiuiu.tuiuiucore import views
from tuiuiu.tuiuiucore.utils import TUIUIU_APPEND_SLASH


if TUIUIU_APPEND_SLASH:
    # If TUIUIU_APPEND_SLASH is True (the default value), we match a
    # (possibly empty) list of path segments ending in slashes.
    # CommonMiddleware will redirect requests without a trailing slash to
    # a URL with a trailing slash
    serve_pattern = r'^((?:[\w\-]+/)*)$'
else:
    # If TUIUIU_APPEND_SLASH is False, allow Tuiuiu to serve pages on URLs
    # with and without trailing slashes
    serve_pattern = r'^([\w\-/]*)$'


TUIUIU_FRONTEND_LOGIN_TEMPLATE = getattr(
    settings, 'TUIUIU_FRONTEND_LOGIN_TEMPLATE', 'tuiuiucore/login.html'
)


urlpatterns = [
    url(r'^_util/authenticate_with_password/(\d+)/(\d+)/$', views.authenticate_with_password,
        name='tuiuiucore_authenticate_with_password'),
    url(r'^_util/login/$', auth_views.login, {'template_name': TUIUIU_FRONTEND_LOGIN_TEMPLATE},
        name='tuiuiucore_login'),

    # Front-end page views are handled through Tuiuiu's core.views.serve
    # mechanism
    url(serve_pattern, views.serve, name='tuiuiu_serve')
]
