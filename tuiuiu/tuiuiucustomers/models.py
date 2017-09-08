from __future__ import absolute_import, unicode_literals

from django.db import models
from tuiuiu.contrib.tenants.models import TenantMixin, DomainMixin


class Customer(TenantMixin):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    created_on = models.DateField(auto_now_add=True)


class Domain(DomainMixin):
    pass
