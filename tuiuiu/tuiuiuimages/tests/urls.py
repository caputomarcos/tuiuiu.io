from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from tuiuiu.tests import dummy_sendfile_backend
from tuiuiu.tuiuiuimages.views.serve import SendFileView, ServeView

urlpatterns = [
    url(r'^actions/serve/(.*)/(\d*)/(.*)/[^/]*', ServeView.as_view(action='serve'), name='tuiuiuimages_serve_action_serve'),
    url(r'^actions/redirect/(.*)/(\d*)/(.*)/[^/]*', ServeView.as_view(action='redirect'), name='tuiuiuimages_serve_action_redirect'),
    url(r'^custom_key/(.*)/(\d*)/(.*)/[^/]*', ServeView.as_view(key='custom'), name='tuiuiuimages_serve_custom_key'),
    url(r'^sendfile/(.*)/(\d*)/(.*)/[^/]*', SendFileView.as_view(), name='tuiuiuimages_sendfile'),
    url(r'^sendfile-dummy/(.*)/(\d*)/(.*)/[^/]*', SendFileView.as_view(backend=dummy_sendfile_backend.sendfile), name='tuiuiuimages_sendfile_dummy'),
]
