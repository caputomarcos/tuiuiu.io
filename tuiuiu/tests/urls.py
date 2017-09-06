from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url

from tuiuiu.api.v2.endpoints import PagesAPIEndpoint
from tuiuiu.api.v2.router import TuiuiuAPIRouter
from tuiuiu.contrib.api import urls as tuiuiuapi_urls
from tuiuiu.contrib.sitemaps import views as sitemaps_views
from tuiuiu.contrib.sitemaps import Sitemap
from tuiuiu.tests.testapp import urls as testapp_urls
from tuiuiu.tuiuiuadmin import urls as tuiuiuadmin_urls
from tuiuiu.tuiuiucore import urls as tuiuiu_urls
from tuiuiu.tuiuiudocs import urls as tuiuiudocs_urls
from tuiuiu.tuiuiudocs.api.v2.endpoints import DocumentsAPIEndpoint
from tuiuiu.tuiuiuimages import urls as tuiuiuimages_urls
from tuiuiu.tuiuiuimages.api.v2.endpoints import ImagesAPIEndpoint
from tuiuiu.tuiuiuimages.tests import urls as tuiuiuimages_test_urls
from tuiuiu.tuiuiusearch import urls as tuiuiusearch_urls


api_router = TuiuiuAPIRouter('tuiuiuapi_v2')
api_router.register_endpoint('pages', PagesAPIEndpoint)
api_router.register_endpoint('images', ImagesAPIEndpoint)
api_router.register_endpoint('documents', DocumentsAPIEndpoint)


urlpatterns = [
    url(r'^admin/', include(tuiuiuadmin_urls)),
    url(r'^search/', include(tuiuiusearch_urls)),
    url(r'^documents/', include(tuiuiudocs_urls)),
    url(r'^testimages/', include(tuiuiuimages_test_urls)),
    url(r'^images/', include(tuiuiuimages_urls)),

    url(r'^api/', include(tuiuiuapi_urls)),
    url(r'^api/v2beta/', api_router.urls),
    url(r'^sitemap\.xml$', sitemaps_views.sitemap),

    url(r'^sitemap-index\.xml$', sitemaps_views.index, {
        'sitemaps': {'pages': Sitemap},
        'sitemap_url_name': 'sitemap',
    }),
    url(r'^sitemap-(?P<section>.+)\.xml$', sitemaps_views.sitemap, name='sitemap'),

    url(r'^testapp/', include(testapp_urls)),

    # For anything not caught by a more specific rule above, hand over to
    # Tuiuiu's serving mechanism
    url(r'', include(tuiuiu_urls)),
]
