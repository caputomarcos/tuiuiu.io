.. _integrating_into_django:

Integrating Tuiuiu into a Django project
=========================================

Tuiuiu provides the ``tuiuiu start`` command and project template to get you started with a new Tuiuiu project as quickly as possible, but it's easy to integrate Tuiuiu into an existing Django project too.

Tuiuiu is currently compatible with Django 1.8, 1.10 and 1.11. First, install the ``tuiuiu`` package from PyPI:

.. code-block:: console

    $ pip install tuiuiu

or add the package to your existing requirements file. This will also install the **Pillow** library as a dependency, which requires libjpeg and zlib - see Pillow's `platform-specific installation instructions <http://pillow.readthedocs.org/en/latest/installation.html#external-libraries>`_.

Settings
--------

In your settings file, add the following apps to ``INSTALLED_APPS``:

.. code-block:: python

    'tuiuiu.tuiuiuforms',
    'tuiuiu.tuiuiuredirects',
    'tuiuiu.tuiuiuembeds',
    'tuiuiu.tuiuiusites',
    'tuiuiu.tuiuiuusers',
    'tuiuiu.tuiuiusnippets',
    'tuiuiu.tuiuiudocs',
    'tuiuiu.tuiuiuimages',
    'tuiuiu.tuiuiusearch',
    'tuiuiu.tuiuiuadmin',
    'tuiuiu.tuiuiucore',

    'modelcluster',
    'taggit',

Add the following entries to ``MIDDLEWARE_CLASSES``:

.. code-block:: python

    'tuiuiu.tuiuiucore.middleware.SiteMiddleware',
    'tuiuiu.tuiuiuredirects.middleware.RedirectMiddleware',

Add a ``STATIC_ROOT`` setting, if your project does not have one already:

.. code-block:: python

    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

Add a ``TUIUIU_SITE_NAME`` - this will be displayed on the main dashboard of the Tuiuiu admin backend:

.. code-block:: python

    TUIUIU_SITE_NAME = 'My Example Site'

Various other settings are available to configure Tuiuiu's behaviour - see :doc:`/advanced_topics/settings`.

URL configuration
-----------------

Now make the following additions to your ``urls.py`` file:

.. code-block:: python

    from tuiuiu.tuiuiuadmin import urls as tuiuiuadmin_urls
    from tuiuiu.tuiuiudocs import urls as tuiuiudocs_urls
    from tuiuiu.tuiuiucore import urls as tuiuiu_urls

    urlpatterns = [
        ...
        url(r'^cms/', include(tuiuiuadmin_urls)),
        url(r'^documents/', include(tuiuiudocs_urls)),
        url(r'^pages/', include(tuiuiu_urls)),
        ...
    ]

The URL paths here can be altered as necessary to fit your project's URL scheme.

``tuiuiuadmin_urls`` provides the admin interface for Tuiuiu. This is separate from the Django admin interface (``django.contrib.admin``); Tuiuiu-only projects typically host the Tuiuiu admin at ``/admin/``, but if this would clash with your project's existing admin backend then an alternative path can be used, such as ``/cms/`` here.

``tuiuiudocs_urls`` is the location from where document files will be served. This can be omitted if you do not intend to use Tuiuiu's document management features.

``tuiuiu_urls`` is the base location from where the pages of your Tuiuiu site will be served. In the above example, Tuiuiu will handle URLs under ``/pages/``, leaving the root URL and other paths to be handled as normal by your Django project. If you want Tuiuiu to handle the entire URL space including the root URL, this can be replaced with:

.. code-block:: python

    url(r'', include(tuiuiu_urls)),

In this case, this should be placed at the end of the ``urlpatterns`` list, so that it does not override more specific URL patterns.

Finally, your project needs to be set up to serve user-uploaded files from ``MEDIA_ROOT``. Your Django project may already have this in place, but if not, add the following snippet to ``urls.py``:

.. code-block:: python

    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns = [
        # ... the rest of your URLconf goes here ...
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

Note that this only works in development mode (``DEBUG = True``); in production, you will need to configure your web server to serve files from ``MEDIA_ROOT``. For further details, see the Django documentation: `Serving files uploaded by a user during development <https://docs.djangoproject.com/en/1.9/howto/static-files/#serving-files-uploaded-by-a-user-during-development>`_ and `Deploying static files <https://docs.djangoproject.com/en/1.9/howto/static-files/deployment/>`_.

With this configuration in place, you are ready to run ``./manage.py migrate`` to create the database tables used by Tuiuiu.

User accounts
-------------

Superuser accounts receive automatic access to the Tuiuiu admin interface; use ``./manage.py createsuperuser`` if you don't already have one. Custom user models are supported, with some restrictions; Tuiuiu uses an extension of Django's permissions framework, so your user model must at minimum inherit from ``AbstractBaseUser`` and ``PermissionsMixin``.

Start developing
----------------

You're now ready to add a new app to your Django project (via ``./manage.py startapp`` - remember to add it to ``INSTALLED_APPS``) and set up page models, as described in :doc:`/getting_started/tutorial`.

Note that there's one small difference when not using the Tuiuiu project template: Tuiuiu creates an initial homepage of the basic type ``Page``, which does not include any content fields beyond the title. You'll probably want to replace this with your own ``HomePage`` class - when you do so, ensure that you set up a site record (under Settings / Sites in the Tuiuiu admin) to point to the new homepage.
