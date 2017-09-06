from __future__ import absolute_import, unicode_literals

from django.apps import AppConfig

from tuiuiu.tuiuiusearch.signal_handlers import register_signal_handlers


class TuiuiuSearchAppConfig(AppConfig):
    name = 'tuiuiu.tuiuiusearch'
    label = 'tuiuiusearch'
    verbose_name = "Tuiuiu search"

    def ready(self):
        register_signal_handlers()
