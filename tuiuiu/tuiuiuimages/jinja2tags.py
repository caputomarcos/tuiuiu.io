from __future__ import absolute_import, unicode_literals

from jinja2.ext import Extension

from .shortcuts import get_rendition_or_not_found


def image(image, filterspec, **attrs):
    if not image:
        return ''

    rendition = get_rendition_or_not_found(image, filterspec)

    if attrs:
        return rendition.img_tag(attrs)
    else:
        return rendition


class TuiuiuImagesExtension(Extension):
    def __init__(self, environment):
        super(TuiuiuImagesExtension, self).__init__(environment)

        self.environment.globals.update({
            'image': image,
        })


# Nicer import names
images = TuiuiuImagesExtension
