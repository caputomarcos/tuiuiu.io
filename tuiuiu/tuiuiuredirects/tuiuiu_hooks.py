from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
from django.contrib.auth.models import Permission
from django.core import urlresolvers
from django.utils.translation import ugettext_lazy as _

from tuiuiu.tuiuiuadmin.menu import MenuItem
from tuiuiu.tuiuiucore import hooks
from tuiuiu.tuiuiuredirects import urls
from tuiuiu.tuiuiuredirects.permissions import permission_policy


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^redirects/', include(urls, app_name='tuiuiuredirects', namespace='tuiuiuredirects')),
    ]


class RedirectsMenuItem(MenuItem):
    def is_shown(self, request):
        return permission_policy.user_has_any_permission(
            request.user, ['add', 'change', 'delete']
        )


@hooks.register('register_settings_menu_item')
def register_redirects_menu_item():
    return RedirectsMenuItem(
        _('Redirects'), urlresolvers.reverse('tuiuiuredirects:index'), classnames='icon icon-redirect', order=800
    )


@hooks.register('register_permissions')
def register_permissions():
    return Permission.objects.filter(content_type__app_label='tuiuiuredirects',
                                     codename__in=['add_redirect', 'change_redirect', 'delete_redirect'])
