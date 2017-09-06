from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from tuiuiu.tuiuiuadmin import urls as tuiuiuadmin_urls
from tuiuiu.tuiuiucore import urls as tuiuiu_urls
from tuiuiu.tuiuiudocs import urls as tuiuiudocs_urls

from tuiuiu.contrib.api import urls as tuiuiuapi_urls

from search import views as search_views


urlpatterns = [
    url(r'^django-admin/', include(admin.site.urls)),

    url(r'^admin/', include(tuiuiuadmin_urls)),
    url(r'^documents/', include(tuiuiudocs_urls)),

    url(r'^search/$', search_views.search, name='search'),

    url(r'^api/', include(tuiuiuapi_urls)),

    # For anything not caught by a more specific rule above, hand over to
    # Tuiuiu's page serving mechanism. This should be the last pattern in
    # the list:
    url(r'', include(tuiuiu_urls)),

    # Alternatively, if you want Tuiuiu pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r'^pages/', include(tuiuiu_urls)),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
