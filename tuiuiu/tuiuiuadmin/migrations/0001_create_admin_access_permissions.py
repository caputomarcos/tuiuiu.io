# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def create_admin_access_permissions(apps, schema_editor):
    ContentType = apps.get_model('contenttypes.ContentType')
    Permission = apps.get_model('auth.Permission')
    Group = apps.get_model('auth.Group')

    # Add a fake content type to hang the 'can access Tuiuiu admin' permission off.
    # The fact that this doesn't correspond to an actual defined model shouldn't matter, I hope...
    tuiuiuadmin_content_type, created = ContentType.objects.get_or_create(
        app_label='tuiuiuadmin',
        model='admin'
    )

    # Create admin permission
    admin_permission, created = Permission.objects.get_or_create(
        content_type=tuiuiuadmin_content_type,
        codename='access_admin',
        name='Can access Tuiuiu admin'
    )

    # Assign it to Editors and Moderators groups
    for group in Group.objects.filter(name__in=['Editors', 'Moderators']):
        group.permissions.add(admin_permission)


def remove_admin_access_permissions(apps, schema_editor):
    """Reverse the above additions of permissions."""
    ContentType = apps.get_model('contenttypes.ContentType')
    Permission = apps.get_model('auth.Permission')
    tuiuiuadmin_content_type = ContentType.objects.get(
        app_label='tuiuiuadmin',
        model='admin',
    )
    # This cascades to Group
    Permission.objects.filter(
        content_type=tuiuiuadmin_content_type,
        codename='access_admin',
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        # We cannot apply and unapply this migration unless GroupCollectionPermission
        # is created. #2529
        ('tuiuiucore', '0026_group_collection_permission'),
    ]

    operations = [
        migrations.RunPython(create_admin_access_permissions, remove_admin_access_permissions),
    ]
