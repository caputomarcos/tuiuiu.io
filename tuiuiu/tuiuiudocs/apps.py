from __future__ import absolute_import, unicode_literals

from django.apps import AppConfig


class TuiuiuDocsAppConfig(AppConfig):
    name = 'tuiuiu.tuiuiudocs'
    label = 'tuiuiudocs'
    verbose_name = "Tuiuiu documents"

    def ready(self):
        from tuiuiu.tuiuiudocs.signal_handlers import register_signal_handlers
        register_signal_handlers()
