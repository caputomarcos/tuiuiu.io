from __future__ import absolute_import, unicode_literals

from django.contrib.auth.models import Permission
from django.db import connection

from tuiuiu.tuiuiucore import hooks

from tuiuiu.contrib.modeladmin.options import modeladmin_register, ModelAdminGroup, ModelAdmin
from tuiuiu.tuiuiucustomers.models import Customer


class CustomerModelAdmin(ModelAdmin):
    model = Customer
    menu_label = 'Customer'  # ditch this to use verbose_name_plural from model
    menu_icon = 'fa-users'  # change as required
    list_display = ('name', 'description', 'created_on')


class CustomerModelAdminGroup(ModelAdminGroup):
    menu_label = 'Customer Misc'
    menu_icon = 'fa-cutlery'  # change as required
    menu_order = 300  # will put in 4th place (000 being 1st, 100 2nd)
    items = (CustomerModelAdmin, )


@hooks.register('register_permissions')
def register_permissions():
    return Permission.objects.filter(content_type__app_label='CustomerModelAdminGroup', codename='access_admin')


# When using a ModelAdminGroup class to group several ModelAdmin classes together,
# you only need to register the ModelAdminGroup class with Tuiuiu:
print(connection.schema_name)
if connection.schema_name == 'public':
    modeladmin_register(CustomerModelAdminGroup)
