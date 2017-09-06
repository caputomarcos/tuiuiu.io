from django.conf import settings
from django.core.management.base import CommandError, BaseCommand

from tuiuiu.tuiuiutenant.management.commands.migrate_schemas import Command as MigrateSchemasCommand
from tuiuiu.tuiuiutenant.utils import django_is_in_test_mode


class Command(BaseCommand):

    def handle(self, *args, **options):
        database = options.get('database', 'default')
        if (settings.DATABASES[database]['ENGINE'] == 'tuiuiu.tuiuiutenant.postgresql_backend'):
            raise CommandError("migrate has been disabled, for database '{0}'. Use migrate_schemas "
                               "instead. Please read the documentation if you don't know why you "
                               "shouldn't call migrate directly!".format(database))
        super(Command, self).handle(*args, **options)


if django_is_in_test_mode():
    Command = MigrateSchemasCommand
