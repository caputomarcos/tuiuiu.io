# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-28 23:49
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tuiuiuusers', '0004_capitalizeverbose'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tuiuiu_userprofile', to=settings.AUTH_USER_MODEL),
        ),
    ]
