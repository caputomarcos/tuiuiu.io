# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def add_page_lock_permission_to_moderators(apps, schema_editor):
    Group = apps.get_model('auth.Group')
    Page = apps.get_model('tuiuiucore.Page')
    GroupPagePermission = apps.get_model('tuiuiucore.GroupPagePermission')

    root_pages = Page.objects.filter(depth=1)

    try:
        moderators_group = Group.objects.get(name='Moderators')

        for page in root_pages:
            GroupPagePermission.objects.create(
                group=moderators_group, page=page, permission_type='lock')

    except Group.DoesNotExist:
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('tuiuiucore', '0004_page_locked'),
    ]

    operations = [
        migrations.RunPython(add_page_lock_permission_to_moderators),
    ]
