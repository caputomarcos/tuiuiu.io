Tuiuiu API Installation
========================


To install, add ``tuiuiu.contrib.tuiuiuapi`` and ``rest_framework`` to ``INSTALLED_APPS`` in your Django settings and configure a URL for it in ``urls.py``:

.. code-block:: python

    # settings.py

    INSTALLED_APPS = [
        ...
        'tuiuiu.contrib.tuiuiuapi',
        'rest_framework',
    ]

    # urls.py

    from tuiuiu.contrib.tuiuiuapi import urls as tuiuiuapi_urls

    urlpatterns = [
        ...

        url(r'^api/', include(tuiuiuapi_urls)),

        ...

        # Ensure that the tuiuiuapi_urls line appears above the default Tuiuiu page serving route
        url(r'', include(tuiuiu_urls)),
    ]
