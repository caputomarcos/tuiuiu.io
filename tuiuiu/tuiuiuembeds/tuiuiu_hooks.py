from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core import urlresolvers
from django.utils.html import format_html

from tuiuiu.tuiuiucore import hooks
from tuiuiu.tuiuiuembeds import urls
from tuiuiu.tuiuiuembeds.rich_text import MediaEmbedHandler


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^embeds/', include(urls, app_name='tuiuiuembeds', namespace='tuiuiuembeds')),
    ]


@hooks.register('insert_editor_js')
def editor_js():
    return format_html(
        """
            <script src="{0}"></script>
            <script>
                window.chooserUrls.embedsChooser = '{1}';
                registerHalloPlugin('hallotuiuiuembeds');
            </script>
        """,
        static('tuiuiuembeds/js/hallo-plugins/hallo-tuiuiuembeds.js'),
        urlresolvers.reverse('tuiuiuembeds:chooser')
    )


@hooks.register('register_rich_text_embed_handler')
def register_media_embed_handler():
    return ('media', MediaEmbedHandler)
