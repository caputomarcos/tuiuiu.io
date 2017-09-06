from __future__ import absolute_import, unicode_literals

from django.apps import AppConfig


class TuiuiuCoreAppConfig(AppConfig):
    name = 'tuiuiu.tuiuiucore'
    label = 'tuiuiucore'
    verbose_name = "Tuiuiu core"

    def ready(self):
        from tuiuiu.tuiuiucore.signal_handlers import register_signal_handlers
        register_signal_handlers()
