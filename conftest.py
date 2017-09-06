from __future__ import absolute_import, unicode_literals

import os
import shutil
import warnings

import django


def pytest_addoption(parser):
    parser.addoption('--deprecation', choices=['all', 'pending', 'imminent', 'none'], default='pending')
    parser.addoption('--postgres', action='store_true')
    parser.addoption('--elasticsearch', action='store_true')


def pytest_configure(config):
    deprecation = config.getoption('deprecation')

    only_tuiuiu = r'^tuiuiu(\.|$)'
    if deprecation == 'all':
        # Show all deprecation warnings from all packages
        warnings.simplefilter('default', DeprecationWarning)
        warnings.simplefilter('default', PendingDeprecationWarning)
    elif deprecation == 'pending':
        # Show all deprecation warnings from tuiuiu
        warnings.filterwarnings('default', category=DeprecationWarning, module=only_tuiuiu)
        warnings.filterwarnings('default', category=PendingDeprecationWarning, module=only_tuiuiu)
    elif deprecation == 'imminent':
        # Show only imminent deprecation warnings from tuiuiu
        warnings.filterwarnings('default', category=DeprecationWarning, module=only_tuiuiu)
    elif deprecation == 'none':
        # Deprecation warnings are ignored by default
        pass

    if config.getoption('postgres'):
        os.environ['DATABASE_ENGINE'] = 'django.db.backends.postgresql_psycopg2'

    # Setup django after processing the pytest arguments so that the env
    # variables are available in the settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tuiuiu.tests.settings')
    django.setup()

    from tuiuiu.tests.settings import MEDIA_ROOT, STATIC_ROOT
    shutil.rmtree(STATIC_ROOT, ignore_errors=True)
    shutil.rmtree(MEDIA_ROOT, ignore_errors=True)


def pytest_unconfigure(config):
    from tuiuiu.tests.settings import MEDIA_ROOT, STATIC_ROOT
    shutil.rmtree(STATIC_ROOT, ignore_errors=True)
    shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
