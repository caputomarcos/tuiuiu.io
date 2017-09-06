from __future__ import absolute_import, unicode_literals

from django.db import models

from tuiuiu.tuiuiutenant.models import TenantMixin


class Customer(TenantMixin):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    created_on = models.DateField(auto_now_add=True)


