# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tuiuiuredirects', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='redirect',
            options={'verbose_name': 'Redirect'},
        ),
        migrations.AlterField(
            model_name='redirect',
            name='site',
            field=models.ForeignKey(
                on_delete=models.CASCADE,
                related_name='redirects', blank=True, editable=False,
                to='tuiuiucore.Site', null=True, verbose_name='Site'
            ),
        ),
    ]
