from __future__ import absolute_import, unicode_literals

import os

import django

DEBUG = False
TUIUIU_ROOT = os.path.dirname(os.path.dirname(__file__))
STATIC_ROOT = os.path.join(TUIUIU_ROOT, 'tests', 'test-static')
MEDIA_ROOT = os.path.join(TUIUIU_ROOT, 'tests', 'test-media')
MEDIA_URL = '/media/'

TIME_ZONE = 'Asia/Tokyo'

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DATABASE_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('DATABASE_NAME', 'tuiuiu'),
        'USER': os.environ.get('DATABASE_USER', None),
        'PASSWORD': os.environ.get('DATABASE_PASS', None),
        'HOST': os.environ.get('DATABASE_HOST', None),

        'TEST': {
            'NAME': os.environ.get('DATABASE_NAME', None),
        }
    }
}

# Add extra options when mssql is used (on for example appveyor)
if DATABASES['default']['ENGINE'] == 'sql_server.pyodbc':
    DATABASES['default']['OPTIONS'] = {
        'driver': 'SQL Server Native Client 11.0',
        'MARS_Connection': 'True',
    }


SECRET_KEY = 'not needed'

ROOT_URLCONF = 'tuiuiu.tests.urls'

STATIC_URL = '/static/'
STATIC_ROOT = STATIC_ROOT

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

USE_TZ = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'tuiuiu.tests.context_processors.do_not_use_static_url',
                'tuiuiu.contrib.settings.context_processors.settings',
            ],
            'debug': True,  # required in order to catch template errors
        },
    },
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'APP_DIRS': False,
        'DIRS': [
            os.path.join(TUIUIU_ROOT, 'tests', 'testapp', 'jinja2_templates'),
        ],
        'OPTIONS': {
            'extensions': [
                'tuiuiu.tuiuiucore.jinja2tags.core',
                'tuiuiu.tuiuiuadmin.jinja2tags.userbar',
                'tuiuiu.tuiuiuimages.jinja2tags.images',
                'tuiuiu.contrib.settings.jinja2tags.settings',
            ],
        },
    },
]

if django.VERSION >= (1, 10):
    MIDDLEWARE = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',

        'tuiuiu.tuiuiucore.middleware.SiteMiddleware',
        'tuiuiu.tuiuiuredirects.middleware.RedirectMiddleware',
    )
else:
    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',

        'tuiuiu.tuiuiucore.middleware.SiteMiddleware',
        'tuiuiu.tuiuiuredirects.middleware.RedirectMiddleware',
    )

INSTALLED_APPS = (
    # Install tuiuiuredirects with its appconfig
    # Theres nothing special about tuiuiuredirects, we just need to have one
    # app which uses AppConfigs to test that hooks load properly
    'tuiuiu.tuiuiuredirects.apps.TuiuiuRedirectsAppConfig',

    'tuiuiu.tests.testapp',
    'tuiuiu.tests.demosite',
    'tuiuiu.tests.customuser',
    'tuiuiu.tests.snippets',
    'tuiuiu.tests.routablepage',
    'tuiuiu.tests.search',
    'tuiuiu.tests.modeladmintest',
    'tuiuiu.contrib.styleguide',
    'tuiuiu.contrib.routablepage',
    'tuiuiu.contrib.frontendcache',
    'tuiuiu.contrib.api',
    'tuiuiu.contrib.searchpromotions',
    'tuiuiu.contrib.settings',
    'tuiuiu.contrib.modeladmin',
    'tuiuiu.contrib.table_block',
    'tuiuiu.tuiuiuforms',
    'tuiuiu.tuiuiusearch',
    'tuiuiu.tuiuiuembeds',
    'tuiuiu.tuiuiuimages',
    'tuiuiu.tuiuiusites',
    'tuiuiu.tuiuiuusers',
    'tuiuiu.tuiuiusnippets',
    'tuiuiu.tuiuiudocs',
    'tuiuiu.tuiuiuadmin',
    'tuiuiu.api.v2',
    'tuiuiu.tuiuiucore',

    'taggit',
    'rest_framework',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'django.contrib.staticfiles',
)


# Using DatabaseCache to make sure that the cache is cleared between tests.
# This prevents false-positives in some tuiuiu core tests where we are
# changing the 'tuiuiu_root_paths' key which may cause future tests to fail.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache',
    }
}

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',  # don't use the intentionally slow default password hasher
)


TUIUIUSEARCH_BACKENDS = {
    'default': {
        'BACKEND': 'tuiuiu.tuiuiusearch.backends.db',
    }
}

AUTH_USER_MODEL = 'customuser.CustomUser'

if django.VERSION >= (1, 10) and os.environ.get('DATABASE_ENGINE') in (
        # Remove next line when Django 1.8 support is dropped.
        'django.db.backends.postgresql_psycopg2',
        'django.db.backends.postgresql'):
    INSTALLED_APPS += ('tuiuiu.contrib.postgres_search',)
    TUIUIUSEARCH_BACKENDS['postgresql'] = {
        'BACKEND': 'tuiuiu.contrib.postgres_search.backend',
    }

if 'ELASTICSEARCH_URL' in os.environ:
    if os.environ.get('ELASTICSEARCH_VERSION') == '5':
        backend = 'tuiuiu.tuiuiusearch.backends.elasticsearch5'
    elif os.environ.get('ELASTICSEARCH_VERSION') == '2':
        backend = 'tuiuiu.tuiuiusearch.backends.elasticsearch2'
    else:
        backend = 'tuiuiu.tuiuiusearch.backends.elasticsearch'

    TUIUIUSEARCH_BACKENDS['elasticsearch'] = {
        'BACKEND': backend,
        'URLS': [os.environ['ELASTICSEARCH_URL']],
        'TIMEOUT': 10,
        'max_retries': 1,
        'AUTO_UPDATE': False,
    }


TUIUIU_SITE_NAME = "Test Site"

# Extra user field for custom user edit and create form tests. This setting
# needs to here because it is used at the module level of tuiuiuusers.forms
# when the module gets loaded. The decorator 'override_settings' does not work
# in this scenario.
TUIUIU_USER_CUSTOM_FIELDS = ['country', 'attachment']

TUIUIUADMIN_RICH_TEXT_EDITORS = {
    'default': {
        'WIDGET': 'tuiuiu.tuiuiuadmin.rich_text.HalloRichTextArea'
    },
    'custom': {
        'WIDGET': 'tuiuiu.tests.testapp.rich_text.CustomRichTextArea'
    },
}
