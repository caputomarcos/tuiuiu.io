from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core import urlresolvers
from django.utils.html import format_html, format_html_join
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext

from tuiuiu.tuiuiuadmin.menu import MenuItem
from tuiuiu.tuiuiuadmin.search import SearchArea
from tuiuiu.tuiuiuadmin.site_summary import SummaryItem
from tuiuiu.tuiuiucore import hooks
from tuiuiu.tuiuiuimages import admin_urls, get_image_model, image_operations
from tuiuiu.tuiuiuimages.api.admin.endpoints import ImagesAdminAPIEndpoint
from tuiuiu.tuiuiuimages.forms import GroupImagePermissionFormSet
from tuiuiu.tuiuiuimages.permissions import permission_policy
from tuiuiu.tuiuiuimages.rich_text import ImageEmbedHandler


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^images/', include(admin_urls, namespace='tuiuiuimages', app_name='tuiuiuimages')),
    ]


@hooks.register('construct_admin_api')
def construct_admin_api(router):
    router.register_endpoint('images', ImagesAdminAPIEndpoint)


class ImagesMenuItem(MenuItem):
    def is_shown(self, request):
        return permission_policy.user_has_any_permission(
            request.user, ['add', 'change', 'delete']
        )


@hooks.register('register_admin_menu_item')
def register_images_menu_item():
    return ImagesMenuItem(
        _('Images'), urlresolvers.reverse('tuiuiuimages:index'),
        name='images', classnames='icon icon-image', order=300
    )


@hooks.register('insert_editor_js')
def editor_js():
    js_files = [
        static('tuiuiuimages/js/hallo-plugins/hallo-tuiuiuimage.js'),
        static('tuiuiuimages/js/image-chooser.js'),
    ]
    js_includes = format_html_join(
        '\n', '<script src="{0}"></script>',
        ((filename, ) for filename in js_files)
    )
    return js_includes + format_html(
        """
        <script>
            window.chooserUrls.imageChooser = '{0}';
            registerHalloPlugin('hallotuiuiuimage');
        </script>
        """,
        urlresolvers.reverse('tuiuiuimages:chooser')
    )


@hooks.register('register_image_operations')
def register_image_operations():
    return [
        ('original', image_operations.DoNothingOperation),
        ('fill', image_operations.FillOperation),
        ('min', image_operations.MinMaxOperation),
        ('max', image_operations.MinMaxOperation),
        ('width', image_operations.WidthHeightOperation),
        ('height', image_operations.WidthHeightOperation),
        ('jpegquality', image_operations.JPEGQualityOperation),
        ('format', image_operations.FormatOperation),
    ]


@hooks.register('register_rich_text_embed_handler')
def register_image_embed_handler():
    return ('image', ImageEmbedHandler)


class ImagesSummaryItem(SummaryItem):
    order = 200
    template = 'tuiuiuimages/homepage/site_summary_images.html'

    def get_context(self):
        return {
            'total_images': get_image_model().objects.count(),
        }

    def is_shown(self):
        return permission_policy.user_has_any_permission(
            self.request.user, ['add', 'change', 'delete']
        )


@hooks.register('construct_homepage_summary_items')
def add_images_summary_item(request, items):
    items.append(ImagesSummaryItem(request))


class ImagesSearchArea(SearchArea):
    def is_shown(self, request):
        return permission_policy.user_has_any_permission(
            request.user, ['add', 'change', 'delete']
        )


@hooks.register('register_admin_search_area')
def register_images_search_area():
    return ImagesSearchArea(
        _('Images'), urlresolvers.reverse('tuiuiuimages:index'),
        name='images',
        classnames='icon icon-image',
        order=200)


@hooks.register('register_group_permission_panel')
def register_image_permissions_panel():
    return GroupImagePermissionFormSet


@hooks.register('describe_collection_contents')
def describe_collection_docs(collection):
    images_count = get_image_model().objects.filter(collection=collection).count()
    if images_count:
        url = urlresolvers.reverse('tuiuiuimages:index') + ('?collection_id=%d' % collection.id)
        return {
            'count': images_count,
            'count_text': ungettext(
                "%(count)s image",
                "%(count)s images",
                images_count
            ) % {'count': images_count},
            'url': url,
        }
