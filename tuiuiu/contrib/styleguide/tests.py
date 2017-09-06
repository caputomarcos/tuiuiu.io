from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.test import TestCase

from tuiuiu.tests.utils import TuiuiuTestUtils


class TestStyleGuide(TestCase, TuiuiuTestUtils):
    def setUp(self):
        self.login()

    def test_styleguide(self):
        response = self.client.get(reverse('styleguide'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'styleguide/base.html')
