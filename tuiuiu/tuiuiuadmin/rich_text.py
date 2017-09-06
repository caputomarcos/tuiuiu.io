from __future__ import absolute_import, unicode_literals

import json

from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.forms import Media, widgets
from django.utils.module_loading import import_string

from tuiuiu.utils.widgets import WidgetWithScript
from tuiuiu.tuiuiuadmin.edit_handlers import RichTextFieldPanel
from tuiuiu.tuiuiucore.rich_text import DbWhitelister, expand_db_html


class HalloRichTextArea(WidgetWithScript, widgets.Textarea):
    def get_panel(self):
        return RichTextFieldPanel

    def render(self, name, value, attrs=None):
        if value is None:
            translated_value = None
        else:
            translated_value = expand_db_html(value, for_editor=True)
        return super(HalloRichTextArea, self).render(name, translated_value, attrs)

    def render_js_init(self, id_, name, value):
        return "makeHalloRichTextEditable({0});".format(json.dumps(id_))

    def value_from_datadict(self, data, files, name):
        original_value = super(HalloRichTextArea, self).value_from_datadict(data, files, name)
        if original_value is None:
            return None
        return DbWhitelister.clean(original_value)

    @property
    def media(self):
        return Media(js=[
            static('tuiuiuadmin/js/vendor/hallo.js'),
            static('tuiuiuadmin/js/hallo-bootstrap.js'),
            static('tuiuiuadmin/js/hallo-plugins/hallo-tuiuiulink.js'),
            static('tuiuiuadmin/js/hallo-plugins/hallo-hr.js'),
            static('tuiuiuadmin/js/hallo-plugins/hallo-requireparagraphs.js'),
        ])


DEFAULT_RICH_TEXT_EDITORS = {
    'default': {
        'WIDGET': 'tuiuiu.tuiuiuadmin.rich_text.HalloRichTextArea'
    }
}


def get_rich_text_editor_widget(name='default'):
    editor_settings = getattr(settings, 'TUIUIUADMIN_RICH_TEXT_EDITORS', DEFAULT_RICH_TEXT_EDITORS)

    editor = editor_settings[name]
    options = editor.get('OPTIONS', None)

    if options is None:
        return import_string(editor['WIDGET'])()

    return import_string(editor['WIDGET'])(options=options)
