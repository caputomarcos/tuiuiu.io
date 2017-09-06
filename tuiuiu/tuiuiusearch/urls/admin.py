from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from tuiuiu.tuiuiusearch.views import queries

urlpatterns = [
    url(r"^queries/chooser/$", queries.chooser, name="queries_chooser"),
    url(r"^queries/chooser/results/$", queries.chooserresults, name="queries_chooserresults"),
]
