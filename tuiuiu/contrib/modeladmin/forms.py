from __future__ import absolute_import, unicode_literals

from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from tuiuiu.tuiuiucore.models import Page


class PageChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        bits = []
        for ancestor in obj.get_ancestors(inclusive=True).exclude(depth=1):
            bits.append(ancestor.get_admin_display_title())
        return mark_safe('<span class="icon icon-arrow-right"></span>'.join(bits))


class ParentChooserForm(forms.Form):
    parent_page = PageChoiceField(
        label=_('Parent page'),
        required=True,
        empty_label=None,
        queryset=Page.objects.none(),
        widget=forms.RadioSelect(),
    )

    def __init__(self, valid_parents_qs, *args, **kwargs):
        self.valid_parents_qs = valid_parents_qs
        super(ParentChooserForm, self).__init__(*args, **kwargs)
        self.fields['parent_page'].queryset = self.valid_parents_qs
