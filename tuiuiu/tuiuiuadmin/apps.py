from __future__ import absolute_import, unicode_literals

from django.apps import AppConfig

from . import checks  # NOQA


class TuiuiuAdminAppConfig(AppConfig):
    name = 'tuiuiu.tuiuiuadmin'
    label = 'tuiuiuadmin'
    verbose_name = "Tuiuiu admin"
