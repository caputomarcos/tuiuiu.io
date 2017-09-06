# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

import tuiuiu.tuiuiucore.models


class Migration(migrations.Migration):

    dependencies = [
        ('tuiuiucore', '0025_collection_initial_data'),
        ('tuiuiudocs', '0004_capitalizeverbose'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='collection',
            field=models.ForeignKey(related_name='+', to='tuiuiucore.Collection', verbose_name='collection', default=tuiuiu.tuiuiucore.models.get_root_collection_id, on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
