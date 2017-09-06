# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tuiuiucore', '0010_change_page_owner_to_null_on_delete'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='first_published_at',
            field=models.DateTimeField(editable=False, null=True),
            preserve_default=True,
        ),
    ]
