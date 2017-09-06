"""An alternative urlconf module where Tuiuiu front-end URLs
are rooted at '/site/' rather than '/'"""

from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url

from tuiuiu.tuiuiuadmin import urls as tuiuiuadmin_urls
from tuiuiu.tuiuiucore import urls as tuiuiu_urls
from tuiuiu.tuiuiudocs import urls as tuiuiudocs_urls
from tuiuiu.tuiuiuimages import urls as tuiuiuimages_urls
from tuiuiu.tuiuiusearch import urls as tuiuiusearch_urls

urlpatterns = [
    url(r'^admin/', include(tuiuiuadmin_urls)),
    url(r'^search/', include(tuiuiusearch_urls)),
    url(r'^documents/', include(tuiuiudocs_urls)),
    url(r'^images/', include(tuiuiuimages_urls)),
    url(r'^site/', include(tuiuiu_urls)),
]
