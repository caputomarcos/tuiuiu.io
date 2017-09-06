from __future__ import absolute_import, unicode_literals

from django.apps import AppConfig

from . import checks  # NOQA


class TuiuiuImagesAppConfig(AppConfig):
    name = 'tuiuiu.tuiuiuimages'
    label = 'tuiuiuimages'
    verbose_name = "Tuiuiu images"

    def ready(self):
        from tuiuiu.tuiuiuimages.signal_handlers import register_signal_handlers
        register_signal_handlers()
