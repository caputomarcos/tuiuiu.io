import argparse
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command, get_commands, load_command_class
from django.db import connection
from tuiuiu.tuiuiutenant.management.commands import InteractiveTenantOption


class Command(InteractiveTenantOption, BaseCommand):
    help = "Wrapper around django commands for use with an individual tenant"

    def run_from_argv(self, argv):
        """
        Changes the option_list to use the options from the wrapped command.
        Adds schema parameter to specify which schema will be used when
        executing the wrapped command.
        """
        # load the command object.
        try:
            app_name = get_commands()[argv[2]]
        except KeyError:
            raise CommandError("Unknown command: %r" % argv[2])

        if isinstance(app_name, BaseCommand):
            # if the command is already loaded, use it directly.
            klass = app_name
        else:
            klass = load_command_class(app_name, argv[2])

        # Ugly, but works. Delete tenant_command from the argv, parse the schema manually
        # and forward the rest of the arguments to the actual command being wrapped.
        del argv[1]
        schema_parser = argparse.ArgumentParser()
        schema_parser.add_argument("-s", "--schema", dest="schema_name", help="specify tenant schema")
        schema_namespace, args = schema_parser.parse_known_args(argv)

        tenant = self.get_tenant_from_options_or_interactive(schema_name=schema_namespace.schema_name)
        connection.set_tenant(tenant)
        klass.run_from_argv(args)

    def handle(self, *args, **options):
        tenant = self.get_tenant_from_options_or_interactive(**options)
        connection.set_tenant(tenant)
        call_command(*args, **options)
