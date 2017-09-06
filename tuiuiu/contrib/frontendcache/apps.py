from __future__ import absolute_import, unicode_literals

from django.apps import AppConfig

from tuiuiu.contrib.frontendcache.signal_handlers import register_signal_handlers


class FrontendcacheAppConfig(AppConfig):
    name = 'tuiuiu.contrib.frontendcache'
    label = 'frontendcache'
    verbose_name = "Tuiuiu frontend cache"

    def ready(self):
        register_signal_handlers()
