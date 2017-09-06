from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url

from tuiuiu.tuiuiucore import hooks

from . import urls


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^settings/', include(urls, app_name='settings', namespace='settings')),
    ]
