.. _styleguide:

UI Styleguide
=============

Developers working on the Tuiuiu UI or creating new UI components may wish to test their work against our Styleguide, which is provided as the contrib module "tuiuiustyleguide".

To install the styleguide module on your site, add it to the list of ``INSTALLED_APPS`` in your settings:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'tuiuiu.contrib.tuiuiustyleguide',
        ...
    )

This will add a 'Styleguide' item to the Settings menu in the admin.

At present the styleguide is static: new UI components must be added to it manually, and there are no hooks into it for other modules to use. We hope to support hooks in the future.

The styleguide doesn't currently provide examples of all the core interface components; notably the Page, Document, Image and Snippet chooser interfaces are not currently represented.
