from __future__ import absolute_import, unicode_literals

# Imported for historical reasons
from tuiuiu import __semver__, __version__  # noqa

default_app_config = 'tuiuiu.tuiuiucore.apps.TuiuiuCoreAppConfig'


def setup():
    import warnings
    from tuiuiu.utils.deprecation import removed_in_next_version_warning

    warnings.simplefilter("default", removed_in_next_version_warning)


setup()
