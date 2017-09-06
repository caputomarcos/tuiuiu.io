# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-10 10:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import tuiuiu.contrib.routablepage.models


class Migration(migrations.Migration):

    dependencies = [
        ('tuiuiucore', '0028_merge'),
        ('routablepagetests', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoutablePageWithoutIndexRouteTest',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tuiuiucore.Page')),
            ],
            options={
                'abstract': False,
            },
            bases=(tuiuiu.contrib.routablepage.models.RoutablePageMixin, 'tuiuiucore.page'),
        ),
    ]
