from __future__ import absolute_import, unicode_literals

from django import forms

from tuiuiu.tuiuiuadmin.forms import TuiuiuAdminPageForm


class ValidatedPageForm(TuiuiuAdminPageForm):
    def clean_foo(self):
        if 'foo' not in self.cleaned_data:
            return

        value = self.cleaned_data['foo']
        if value != 'bar':
            raise forms.ValidationError('Field foo must be bar')
        return value
