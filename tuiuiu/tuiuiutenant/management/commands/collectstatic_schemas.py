from tuiuiu.tuiuiutenant.management.commands import BaseTenantCommand


class Command(BaseTenantCommand):
    COMMAND_NAME = 'collectstatic'
