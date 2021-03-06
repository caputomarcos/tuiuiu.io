.. _frontend_cache_purging:

Frontend cache invalidator
==========================

.. versionchanged:: 0.7

   * Multiple backend support added
   * Cloudflare support added

.. versionchanged:: 1.7

   * Amazon CloudFront support added

Many websites use a frontend cache such as Varnish, Squid, Cloudflare or CloudFront to gain extra performance. The downside of using a frontend cache though is that they don't respond well to updating content and will often keep an old version of a page cached after it has been updated.

This document describes how to configure Tuiuiu to purge old versions of pages from a frontend cache whenever a page gets updated.


Setting it up
-------------

Firstly, add ``"tuiuiu.contrib.tuiuiufrontendcache"`` to your INSTALLED_APPS:

 .. code-block:: python

     INSTALLED_APPS = [
        ...

        "tuiuiu.contrib.tuiuiufrontendcache"
     ]

.. versionchanged:: 0.8

    Signal handlers are now automatically registered

The ``tuiuiufrontendcache`` module provides a set of signal handlers which will automatically purge the cache whenever a page is published or deleted. These signal handlers are automatically registered when the ``tuiuiu.contrib.tuiuiufrontendcache`` app is loaded.


Varnish/Squid
^^^^^^^^^^^^^

Add a new item into the ``TUIUIUFRONTENDCACHE`` setting and set the ``BACKEND`` parameter to ``tuiuiu.contrib.tuiuiufrontendcache.backends.HTTPBackend``. This backend requires an extra parameter ``LOCATION`` which points to where the cache is running (this must be a direct connection to the server and cannot go through another proxy).

.. code-block:: python

    # settings.py

    TUIUIUFRONTENDCACHE = {
        'varnish': {
            'BACKEND': 'tuiuiu.contrib.tuiuiufrontendcache.backends.HTTPBackend',
            'LOCATION': 'http://localhost:8000',
        },
    }


Finally, make sure you have configured your frontend cache to accept PURGE requests:

 - `Varnish <https://www.varnish-cache.org/docs/3.0/tutorial/purging.html>`_
 - `Squid <http://wiki.squid-cache.org/SquidFaq/OperatingSquid#How_can_I_purge_an_object_from_my_cache.3F>`_


.. _frontendcache_cloudflare:

Cloudflare
^^^^^^^^^^

Firstly, you need to register an account with Cloudflare if you haven't already got one. You can do this here: `Cloudflare Sign up <https://www.cloudflare.com/sign-up>`_

Add an item into the ``TUIUIUFRONTENDCACHE`` and set the ``BACKEND`` parameter to ``tuiuiu.contrib.tuiuiufrontendcache.backends.CloudflareBackend``. This backend requires three extra parameters, ``EMAIL`` (your Cloudflare account email), ``TOKEN`` (your API token from Cloudflare), and ``ZONEID`` (for zone id for your domain, see below).

To find the ``ZONEID`` for your domain, read the `Cloudflare API Documentation <https://api.cloudflare.com/#getting-started-resource-ids>`_


.. code-block:: python

    # settings.py

    TUIUIUFRONTENDCACHE = {
        'cloudflare': {
            'BACKEND': 'tuiuiu.contrib.tuiuiufrontendcache.backends.CloudflareBackend',
            'EMAIL': 'your-cloudflare-email-address@example.com',
            'TOKEN': 'your cloudflare api token',
            'ZONEID': 'your cloudflare domain zone id',
        },
    }

.. _frontendcache_aws_cloudfront:

Amazon CloudFront
^^^^^^^^^^^^^^^^^

Within Amazon Web Services you will need at least one CloudFront web distribution. If you don't have one, you can get one here: `CloudFront getting started <https://aws.amazon.com/cloudfront/>`_

Add an item into the ``TUIUIUFRONTENDCACHE`` and set the ``BACKEND`` parameter to ``tuiuiu.contrib.tuiuiufrontendcache.backends.CloudfrontBackend``. This backend requires one extra parameter, ``DISTRIBUTION_ID`` (your CloudFront generated distribution id).

.. code-block:: python

    TUIUIUFRONTENDCACHE = {
        'cloudfront': {
            'BACKEND': 'tuiuiu.contrib.tuiuiufrontendcache.backends.CloudfrontBackend',
            'DISTRIBUTION_ID': 'your-distribution-id',
        },
    }

Configuration of credentials can done in multiple ways. You won't need to store them in your Django settings file. You can read more about this here: `Boto 3 Docs <http://boto3.readthedocs.org/en/latest/guide/configuration.html>`_

In case you run multiple sites with Tuiuiu and each site has its CloudFront distribution, provide a mapping instead of a single distribution. Make sure the mapping matches with the hostnames provided in your site settings.

.. code-block:: python

    TUIUIUFRONTENDCACHE = {
        'cloudfront': {
            'BACKEND': 'tuiuiu.contrib.tuiuiufrontendcache.backends.CloudfrontBackend',
            'DISTRIBUTION_ID': {
                'www.tuiuiu.io': 'your-distribution-id',
                'www.madewithtuiuiu.org': 'your-distribution-id',
            },
        },
    }

.. note::
    In most cases, absolute URLs with ``www`` prefixed domain names should be used in your mapping. Only drop the ``www`` prefix if you're absolutely sure you're not using it (e.g. a subdomain).

Advanced usage
--------------

Invalidating more than one URL per page
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, Tuiuiu will only purge one URL per page. If your page has more than one URL to be purged, you will need to override the ``get_cached_paths`` method on your page type.

.. code-block:: python

    class BlogIndexPage(Page):
        def get_blog_items(self):
            # This returns a Django paginator of blog items in this section
            return Paginator(self.get_children().live().type(BlogPage), 10)

        def get_cached_paths(self):
            # Yield the main URL
            yield '/'

            # Yield one URL per page in the paginator to make sure all pages are purged
            for page_number in range(1, self.get_blog_items().num_pages + 1):
                yield '/?page=' + str(page_number)


Invalidating index pages
^^^^^^^^^^^^^^^^^^^^^^^^

Another problem is pages that list other pages (such as a blog index) will not be purged when a blog entry gets added, changed or deleted. You may want to purge the blog index page so the updates are added into the listing quickly.

This can be solved by using the ``purge_page_from_cache`` utility function which can be found in the ``tuiuiu.contrib.tuiuiufrontendcache.utils`` module.

Let's take the the above BlogIndexPage as an example. We need to register a signal handler to run when one of the BlogPages get updated/deleted. This signal handler should call the ``purge_page_from_cache`` function on all BlogIndexPages that contain the BlogPage being updated/deleted.


.. code-block:: python

    # models.py
    from django.dispatch import receiver
    from django.db.models.signals import pre_delete

    from tuiuiu.tuiuiucore.signals import page_published
    from tuiuiu.contrib.tuiuiufrontendcache.utils import purge_page_from_cache


    ...


    def blog_page_changed(blog_page):
        # Find all the live BlogIndexPages that contain this blog_page
        for blog_index in BlogIndexPage.objects.live():
            if blog_page in blog_index.get_blog_items().object_list:
                # Purge this blog index
                purge_page_from_cache(blog_index)


    @receiver(page_published, sender=BlogPage):
    def blog_published_handler(instance):
        blog_page_changed(instance)


    @receiver(pre_delete, sender=BlogPage)
    def blog_deleted_handler(instance):
        blog_page_changed(instance)


Invalidating individual URLs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``tuiuiu.contrib.tuiuiufrontendcache.utils`` provides another function called ``purge_url_from_cache``. As the name suggests, this purges an individual URL from the cache.

For example, this could be useful for purging a single page of blogs:

.. code-block:: python

    from tuiuiu.contrib.tuiuiufrontendcache.utils import purge_url_from_cache

    # Purge the first page of the blog index
    purge_url_from_cache(blog_index.url + '?page=1')
