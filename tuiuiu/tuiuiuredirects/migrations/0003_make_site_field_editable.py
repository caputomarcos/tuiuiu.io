# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tuiuiuredirects', '0002_add_verbose_names'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redirect',
            name='site',
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                null=True, to='tuiuiucore.Site', verbose_name='Site', blank=True, related_name='redirects'
            ),
        ),
    ]
