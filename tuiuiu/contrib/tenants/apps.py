from django.conf import settings
from django.apps import AppConfig
from django.core.exceptions import ImproperlyConfigured
from tuiuiu.contrib.tenants.utils import get_public_schema_name, get_tenant_model


recommended_config = """
Warning: You should put 'tenants' at the end of INSTALLED_APPS:
INSTALLED_APPS = TUIUIU_TENANT_APPS + TUIUIU_SHARED_APPS + ('tenants',)
This is necessary to overwrite built-in django management commands with
their schema-aware implementations.
"""


class TenantsConfig(AppConfig):
    name = 'tenants'
    verbose_name = "Tuiuiu tenants"

    def ready(self):
        from django.db import connection

        # Test for configuration recommendations. These are best practices,
        # they avoid hard to find bugs and unexpected behaviour.
        if not hasattr(settings, 'TUIUIU_TENANT_APPS'):
            raise ImproperlyConfigured('TUIUIU_TENANT_APPS setting not set')

        if not settings.TUIUIU_TENANT_APPS:
            raise ImproperlyConfigured("TUIUIU_TENANT_APPS is empty. "
                                       "Maybe you don't need this app?")

        if not hasattr(settings, 'TUIUIU_TENANT_MODEL'):
            raise ImproperlyConfigured('TUIUIU_TENANT_MODEL setting not set')

        if 'tenants.routers.TenantSyncRouter' not in settings.DATABASE_ROUTERS:
            raise ImproperlyConfigured("DATABASE_ROUTERS setting must contain "
                                       "'tenants.routers.TenantSyncRouter'.")

        if hasattr(settings, 'PG_EXTRA_SEARCH_PATHS'):
            if get_public_schema_name() in settings.PG_EXTRA_SEARCH_PATHS:
                raise ImproperlyConfigured(
                    "%s can not be included on PG_EXTRA_SEARCH_PATHS."
                    % get_public_schema_name())

            # make sure no tenant schema is in settings.PG_EXTRA_SEARCH_PATHS

            # first check that the model table is created
            model = get_tenant_model()
            c = connection.cursor()
            c.execute(
                'SELECT 1 FROM information_schema.tables WHERE table_name = %s;',
                [model._meta.db_table]
            )
            if c.fetchone():
                invalid_schemas = set(settings.PG_EXTRA_SEARCH_PATHS).intersection(
                    model.objects.all().values_list('schema_name', flat=True))
                if invalid_schemas:
                    raise ImproperlyConfigured(
                        "Do not include tenant schemas (%s) on PG_EXTRA_SEARCH_PATHS."
                        % list(invalid_schemas))