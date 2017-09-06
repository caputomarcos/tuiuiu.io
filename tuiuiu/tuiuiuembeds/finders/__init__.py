import sys
from importlib import import_module

from django.utils.module_loading import import_string
from django.utils import six
from django.conf import settings


MOVED_FINDERS = {
    'tuiuiu.tuiuiuembeds.embeds.embedly': 'tuiuiu.tuiuiuembeds.finders.embedly',
    'tuiuiu.tuiuiuembeds.embeds.oembed': 'tuiuiu.tuiuiuembeds.finders.oembed',
}


def import_finder(dotted_path):
    """
    Imports a finder function from a dotted path. If the dotted path points to a
    module, that module is imported and its "find_embed" function returned.

    If not, this will assume the dotted path points to directly a function and
    will attempt to import that instead.
    """
    try:
        finder_module = import_module(dotted_path)
        return finder_module.find_embed
    except ImportError as e:
        try:
            return import_string(dotted_path)
        except ImportError:
            six.reraise(ImportError, e, sys.exc_info()[2])


def get_default_finder():
    # Check if the user has set the embed finder manually
    if hasattr(settings, 'TUIUIUEMBEDS_EMBED_FINDER'):
        finder_name = settings.TUIUIUEMBEDS_EMBED_FINDER

        if finder_name in MOVED_FINDERS:
            finder_name = MOVED_FINDERS[finder_name]

    elif hasattr(settings, 'TUIUIUEMBEDS_EMBEDLY_KEY'):
        # Default to Embedly as an embedly key is set
        finder_name = 'tuiuiu.tuiuiuembeds.finders.embedly'

    else:
        # Default to oembed
        finder_name = 'tuiuiu.tuiuiuembeds.finders.oembed'

    return import_finder(finder_name)
