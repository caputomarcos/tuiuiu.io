from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from tuiuiu.api.v2.router import TuiuiuAPIRouter
from tuiuiu.tuiuiucore import hooks

from .endpoints import PagesAdminAPIEndpoint

admin_api = TuiuiuAPIRouter('tuiuiuadmin_api_v1')
admin_api.register_endpoint('pages', PagesAdminAPIEndpoint)

for fn in hooks.get_hooks('construct_admin_api'):
    fn(admin_api)

urlpatterns = [
    url(r'^v2beta/', admin_api.urls),
]
