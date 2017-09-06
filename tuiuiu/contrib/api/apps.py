from __future__ import absolute_import, unicode_literals

from django.apps import AppConfig, apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class TuiuiuAPIAppConfig(AppConfig):
    name = 'tuiuiu.contrib.api'
    label = 'tuiuiuapi_v1'
    verbose_name = "Tuiuiu API"

    def ready(self):
        # Install cache purging signal handlers
        if getattr(settings, 'TUIUIUAPI_USE_FRONTENDCACHE', False):
            if apps.is_installed('tuiuiu.contrib.frontendcache'):
                from tuiuiu.contrib.api.signal_handlers import register_signal_handlers
                register_signal_handlers()
            else:
                raise ImproperlyConfigured(
                    "The setting 'TUIUIUAPI_USE_FRONTENDCACHE' is True but "
                    "'tuiuiu.contrib.frontendcache' is not in INSTALLED_APPS."
                )

        if not apps.is_installed('rest_framework'):
            raise ImproperlyConfigured(
                "The 'tuiuiuapi' module requires Django REST framework. "
                "Please add 'rest_framework' to INSTALLED_APPS."
            )
