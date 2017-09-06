from pkg_resources import parse_version

from django.utils.html import format_html
from django.conf import settings

from tuiuiu.tuiuiucore import hooks
from tuiuiu.tuiuiucore import __version__ as TUIUIU_VERSION


def import_tuiuiufontawesome_stylesheet():
    elem = '<link rel="stylesheet" href="%stuiuiufontawesome/css/tuiuiufontawesome.css">' % settings.STATIC_URL
    return format_html(elem)

# New Tuiuiu versions support importing CSS throughout the admin.
# Fall back to the old hook (editor screen only) for older versions.
if parse_version(TUIUIU_VERSION) >= parse_version('1.4'):
    admin_stylesheet_hook = 'insert_global_admin_css'
else:
    admin_stylesheet_hook = 'insert_editor_css'

hooks.register(admin_stylesheet_hook, import_tuiuiufontawesome_stylesheet)
