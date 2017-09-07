from .base import MigrationExecutor, run_migrations


class StandardExecutor(MigrationExecutor):
    codename = 'standard'

    def run_migrations(self, tenants=None):
        tenants = tenants or []

        if self.PUBLIC_SCHEMA_NAME in tenants:
            run_migrations(self.args, self.options, self.codename, self.PUBLIC_SCHEMA_NAME)
            tenants.pop(tenants.index(self.PUBLIC_SCHEMA_NAME))

        for idx, schema_name in enumerate(tenants):
            run_migrations(self.args, self.options, self.codename, schema_name, idx=idx, count=len(tenants))
