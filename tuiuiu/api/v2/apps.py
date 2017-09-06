from __future__ import absolute_import, unicode_literals

from django.apps import AppConfig, apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class TuiuiuAPIV2AppConfig(AppConfig):
    name = 'tuiuiu.api.v2'
    label = 'tuiuiuapi_v2'
    verbose_name = "Tuiuiu API v2"

    def ready(self):
        # Install cache purging signal handlers
        if getattr(settings, 'TUIUIUAPI_USE_FRONTENDCACHE', False):
            if apps.is_installed('tuiuiu.contrib.frontendcache'):
                from tuiuiu.api.v2.signal_handlers import register_signal_handlers
                register_signal_handlers()
            else:
                raise ImproperlyConfigured("The setting 'TUIUIUAPI_USE_FRONTENDCACHE' is True but 'tuiuiu.contrib.frontendcache' is not in INSTALLED_APPS.")
