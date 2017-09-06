from __future__ import absolute_import, unicode_literals

import os

from django.core.checks import Error, Warning, register


@register()
def css_install_check(app_configs, **kwargs):
    errors = []

    css_path = os.path.join(
        os.path.dirname(__file__), 'static', 'tuiuiuadmin', 'css', 'normalize.css'
    )

    if not os.path.isfile(css_path):
        error_hint = """
            Most likely you are running a development (non-packaged) copy of
            Tuiuiu and have not built the static assets -
            see http://docs.tuiuiu.io/en/latest/contributing/developing.html

            File not found: %s
        """ % css_path

        errors.append(
            Warning(
                "CSS for the Tuiuiu admin is missing",
                hint=error_hint,
                id='tuiuiuadmin.W001',
            )
        )
    return errors


@register()
def base_form_class_check(app_configs, **kwargs):
    from tuiuiu.tuiuiuadmin.forms import TuiuiuAdminPageForm
    from tuiuiu.tuiuiucore.models import get_page_models

    errors = []

    for cls in get_page_models():
        if not issubclass(cls.base_form_class, TuiuiuAdminPageForm):
            errors.append(Error(
                "{}.base_form_class does not extend TuiuiuAdminPageForm".format(
                    cls.__name__),
                hint="Ensure that {}.{} extends TuiuiuAdminPageForm".format(
                    cls.base_form_class.__module__,
                    cls.base_form_class.__name__),
                obj=cls,
                id='tuiuiuadmin.E001'))

    return errors


@register()
def get_form_class_check(app_configs, **kwargs):
    from tuiuiu.tuiuiuadmin.forms import TuiuiuAdminPageForm
    from tuiuiu.tuiuiucore.models import get_page_models

    errors = []

    for cls in get_page_models():
        edit_handler = cls.get_edit_handler()
        if not issubclass(edit_handler.get_form_class(cls), TuiuiuAdminPageForm):
            errors.append(Error(
                "{cls}.get_edit_handler().get_form_class({cls}) does not extend TuiuiuAdminPageForm".format(
                    cls=cls.__name__),
                hint="Ensure that the EditHandler for {cls} creates a subclass of TuiuiuAdminPageForm".format(
                    cls=cls.__name__),
                obj=cls,
                id='tuiuiuadmin.E002'))

    return errors
