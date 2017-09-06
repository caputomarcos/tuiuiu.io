from __future__ import absolute_import, unicode_literals

from django.test import TestCase

from tuiuiu.tests.utils import TuiuiuTestUtils


class AdminAPITestCase(TestCase, TuiuiuTestUtils):
    def setUp(self):
        self.login()
