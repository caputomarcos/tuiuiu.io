from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


default_app_config = 'tuiuiu.tuiuiuimages.apps.TuiuiuImagesAppConfig'


def get_image_model_string():
    """
    Get the dotted ``app.Model`` name for the image model as a string.
    Useful for developers making Tuiuiu plugins that need to refer to the
    image model, such as in foreign keys, but the model itself is not required.
    """
    return getattr(settings, 'TUIUIUIMAGES_IMAGE_MODEL', 'tuiuiuimages.Image')


def get_image_model():
    """
    Get the image model from the ``TUIUIUIMAGES_IMAGE_MODEL`` setting.
    Useful for developers making Tuiuiu plugins that need the image model.
    Defaults to the standard :class:`~tuiuiu.tuiuiuimages.models.Image` model
    if no custom model is defined.
    """
    from django.apps import apps
    model_string = get_image_model_string()
    try:
        return apps.get_model(model_string)
    except ValueError:
        raise ImproperlyConfigured("TUIUIUIMAGES_IMAGE_MODEL must be of the form 'app_label.model_name'")
    except LookupError:
        raise ImproperlyConfigured(
            "TUIUIUIMAGES_IMAGE_MODEL refers to model '%s' that has not been installed" % model_string
        )
