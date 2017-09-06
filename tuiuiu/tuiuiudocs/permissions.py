from __future__ import absolute_import, unicode_literals

from tuiuiu.tuiuiucore.permission_policies.collections import CollectionOwnershipPermissionPolicy
from tuiuiu.tuiuiudocs.models import Document, get_document_model

permission_policy = CollectionOwnershipPermissionPolicy(
    get_document_model(),
    auth_model=Document,
    owner_field_name='uploaded_by_user'
)
