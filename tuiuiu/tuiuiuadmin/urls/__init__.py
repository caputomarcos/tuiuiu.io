from django.conf.urls import url, include
from django.views.decorators.cache import cache_control

from tuiuiu.tuiuiuadmin.urls import pages as tuiuiuadmin_pages_urls
from tuiuiu.tuiuiuadmin.urls import collections as tuiuiuadmin_collections_urls
from tuiuiu.tuiuiuadmin.urls import password_reset as tuiuiuadmin_password_reset_urls
from tuiuiu.tuiuiuadmin.views import account, chooser, home, pages, tags, userbar
from tuiuiu.tuiuiuadmin.api import urls as api_urls
from tuiuiu.tuiuiucore import hooks
from tuiuiu.utils.urlpatterns import decorate_urlpatterns
from tuiuiu.tuiuiuadmin.decorators import require_admin_access


urlpatterns = [
    url(r'^$', home.home, name='tuiuiuadmin_home'),

    url(r'api/', include(api_urls)),

    url(r'^failwhale/$', home.error_test, name='tuiuiuadmin_error_test'),

    # TODO: Move into tuiuiuadmin_pages namespace
    url(r'^pages/$', pages.index, name='tuiuiuadmin_explore_root'),
    url(r'^pages/(\d+)/$', pages.index, name='tuiuiuadmin_explore'),

    url(r'^pages/', include(tuiuiuadmin_pages_urls, app_name='tuiuiuadmin_pages', namespace='tuiuiuadmin_pages')),

    # TODO: Move into tuiuiuadmin_pages namespace
    url(r'^choose-page/$', chooser.browse, name='tuiuiuadmin_choose_page'),
    url(r'^choose-page/(\d+)/$', chooser.browse, name='tuiuiuadmin_choose_page_child'),
    url(r'^choose-page/search/$', chooser.search, name='tuiuiuadmin_choose_page_search'),
    url(r'^choose-external-link/$', chooser.external_link, name='tuiuiuadmin_choose_page_external_link'),
    url(r'^choose-email-link/$', chooser.email_link, name='tuiuiuadmin_choose_page_email_link'),

    url(r'^tag-autocomplete/$', tags.autocomplete, name='tuiuiuadmin_tag_autocomplete'),

    url(r'^collections/', include(tuiuiuadmin_collections_urls, namespace='tuiuiuadmin_collections')),

    url(r'^account/$', account.account, name='tuiuiuadmin_account'),
    url(r'^account/change_password/$', account.change_password, name='tuiuiuadmin_account_change_password'),
    url(
        r'^account/notification_preferences/$',
        account.notification_preferences,
        name='tuiuiuadmin_account_notification_preferences'
    ),
    url(
        r'^account/language_preferences/$',
        account.language_preferences,
        name='tuiuiuadmin_account_language_preferences'
    ),
    url(r'^logout/$', account.logout, name='tuiuiuadmin_logout'),
]


# Import additional urlpatterns from any apps that define a register_admin_urls hook
for fn in hooks.get_hooks('register_admin_urls'):
    urls = fn()
    if urls:
        urlpatterns += urls


# Add "tuiuiuadmin.access_admin" permission check
urlpatterns = decorate_urlpatterns(urlpatterns, require_admin_access)


# These url patterns do not require an authenticated admin user
urlpatterns += [
    url(r'^login/$', account.login, name='tuiuiuadmin_login'),

    # These two URLs have the "permission_required" decorator applied directly
    # as they need to fail with a 403 error rather than redirect to the login page
    url(r'^userbar/(\d+)/$', userbar.for_frontend, name='tuiuiuadmin_userbar_frontend'),
    url(r'^userbar/moderation/(\d+)/$', userbar.for_moderation, name='tuiuiuadmin_userbar_moderation'),

    # Password reset
    url(r'^password_reset/', include(tuiuiuadmin_password_reset_urls)),
]

# Decorate all views with cache settings to prevent caching
urlpatterns = decorate_urlpatterns(
    urlpatterns,
    cache_control(private=True, no_cache=True, no_store=True, max_age=0)
)
