from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.contrib import admin

from tuiuiu.tuiuiudocs.models import Document

if hasattr(settings, 'TUIUIUDOCS_DOCUMENT_MODEL') and settings.TUIUIUDOCS_DOCUMENT_MODEL != 'tuiuiudocs.Document':
    # This installation provides its own custom document class;
    # to avoid confusion, we won't expose the unused tuiuiudocs.Document class
    # in the admin.
    pass
else:
    admin.site.register(Document)
