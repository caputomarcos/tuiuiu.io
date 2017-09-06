from __future__ import absolute_import, unicode_literals

import os

from django.core.checks import Warning, register
from django.utils.lru_cache import lru_cache
from willow.image import Image


@lru_cache()
def has_jpeg_support():
    tuiuiu_jpg = os.path.join(os.path.dirname(__file__), 'check_files', 'tuiuiu.jpg')
    succeeded = True

    with open(tuiuiu_jpg, 'rb') as f:
        try:
            Image.open(f)
        except (IOError, Image.LoaderError):
            succeeded = False

    return succeeded


@lru_cache()
def has_png_support():
    tuiuiu_png = os.path.join(os.path.dirname(__file__), 'check_files', 'tuiuiu.png')
    succeeded = True

    with open(tuiuiu_png, 'rb') as f:
        try:
            Image.open(f)
        except (IOError, Image.LoaderError):
            succeeded = False

    return succeeded


@register()
def image_library_check(app_configs, **kwargs):
    errors = []

    if not has_jpeg_support():
        errors.append(
            Warning(
                'JPEG image support is not available',
                hint="Check that the 'libjpeg' library is installed, then reinstall Pillow."
            )
        )

    if not has_png_support():
        errors.append(
            Warning(
                'PNG image support is not available',
                hint="Check that the 'zlib' library is installed, then reinstall Pillow."
            )
        )

    return errors
