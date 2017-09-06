# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

import tuiuiu.tuiuiucore.models


class Migration(migrations.Migration):

    dependencies = [
        ('tuiuiucore', '0026_group_collection_permission'),
        ('tuiuiuimages', '0010_change_on_delete_behaviour'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='collection',
            field=models.ForeignKey(to='tuiuiucore.Collection', verbose_name='collection', default=tuiuiu.tuiuiucore.models.get_root_collection_id, related_name='+', on_delete=models.CASCADE),
        ),
    ]
