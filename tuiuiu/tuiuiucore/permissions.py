from __future__ import absolute_import, unicode_literals

from tuiuiu.tuiuiucore.models import Collection, Site
from tuiuiu.tuiuiucore.permission_policies import ModelPermissionPolicy

site_permission_policy = ModelPermissionPolicy(Site)
collection_permission_policy = ModelPermissionPolicy(Collection)
