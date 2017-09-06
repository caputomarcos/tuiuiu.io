from __future__ import absolute_import, unicode_literals

from django.utils.functional import cached_property
from django.utils.html import format_html

from tuiuiu.tuiuiucore.blocks import ChooserBlock


class DocumentChooserBlock(ChooserBlock):
    @cached_property
    def target_model(self):
        from tuiuiu.tuiuiudocs.models import get_document_model
        return get_document_model()

    @cached_property
    def widget(self):
        from tuiuiu.tuiuiudocs.widgets import AdminDocumentChooser
        return AdminDocumentChooser

    def render_basic(self, value, context=None):
        if value:
            return format_html('<a href="{0}">{1}</a>', value.url, value.title)
        else:
            return ''

    class Meta:
        icon = "doc-empty"
