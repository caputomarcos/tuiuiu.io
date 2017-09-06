from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
from django.contrib.auth.models import Permission
from django.core import urlresolvers
from django.utils.translation import ugettext_lazy as _

from tuiuiu.contrib.searchpromotions import admin_urls
from tuiuiu.tuiuiuadmin.menu import MenuItem
from tuiuiu.tuiuiucore import hooks


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^searchpicks/', include(admin_urls, app_name='searchpromotions', namespace='searchpromotions')),
    ]


class SearchPicksMenuItem(MenuItem):
    def is_shown(self, request):
        return (
            request.user.has_perm('searchpromotions.add_searchpromotion') or
            request.user.has_perm('searchpromotions.change_searchpromotion') or
            request.user.has_perm('searchpromotions.delete_searchpromotion')
        )


@hooks.register('register_settings_menu_item')
def register_search_picks_menu_item():
    return SearchPicksMenuItem(
        _('Promoted search results'),
        urlresolvers.reverse('searchpromotions:index'),
        classnames='icon icon-pick', order=900
    )


@hooks.register('register_permissions')
def register_permissions():
    return Permission.objects.filter(
        content_type__app_label='searchpromotions',
        codename__in=['add_searchpromotion', 'change_searchpromotion', 'delete_searchpromotion']
    )
