# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('tuiuiusearch', '0002_add_verbose_names'),
    ]

    operations = [
        # EditorsPicks have been moved to the "searchpromotions" module.

        # Remove EditorsPick from tuiuiusearch but don't drop the underlying table
        # so searchpromotions can pick it up in its initial migration.

        # If searchpromotions isn't installed, this table will remain
        # in the database unmanaged until it is. This could potentially happen
        # at any point in the future so it's important to keep this behaviour
        # even if we decide to squash these migrations.
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveField(
                    model_name='editorspick',
                    name='page',
                ),
                migrations.RemoveField(
                    model_name='editorspick',
                    name='query',
                ),
                migrations.DeleteModel(
                    name='EditorsPick',
                ),
            ],
            database_operations=[],
        )
    ]
