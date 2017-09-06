from __future__ import absolute_import, unicode_literals

# The edit_handlers module extends Page with some additional attributes required by
# tuiuiuadmin (namely, base_form_class and get_edit_handler). Importing this within
# tuiuiuadmin.models ensures that this happens in advance of running tuiuiuadmin's
# system checks.
from tuiuiu.tuiuiuadmin import edit_handlers  # NOQA
