# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tuiuiuredirects', '0003_make_site_field_editable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redirect',
            name='old_path',
            field=models.CharField(verbose_name='Redirect from', max_length=255, db_index=True),
        ),
        migrations.AlterUniqueTogether(
            name='redirect',
            unique_together=set([('old_path', 'site')]),
        ),
    ]
