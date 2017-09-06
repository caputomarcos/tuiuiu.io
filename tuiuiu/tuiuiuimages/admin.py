from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.contrib import admin

from tuiuiu.tuiuiuimages.models import Image

if hasattr(settings, 'TUIUIUIMAGES_IMAGE_MODEL') and settings.TUIUIUIMAGES_IMAGE_MODEL != 'tuiuiuimages.Image':
    # This installation provides its own custom image class;
    # to avoid confusion, we won't expose the unused tuiuiuimages.Image class
    # in the admin.
    pass
else:
    admin.site.register(Image)
