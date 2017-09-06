from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url

from tuiuiu.tuiuiucore import hooks
from tuiuiu.tuiuiusearch.urls import admin as admin_urls


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^search/', include(admin_urls, namespace='tuiuiusearch_admin')),
    ]
