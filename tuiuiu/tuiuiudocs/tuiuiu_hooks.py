from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core import urlresolvers
from django.template.response import TemplateResponse
from django.utils.html import format_html, format_html_join
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext

from tuiuiu.tuiuiuadmin.menu import MenuItem
from tuiuiu.tuiuiuadmin.search import SearchArea
from tuiuiu.tuiuiuadmin.site_summary import SummaryItem
from tuiuiu.tuiuiucore import hooks
from tuiuiu.tuiuiucore.models import BaseViewRestriction
from tuiuiu.tuiuiucore.tuiuiu_hooks import require_tuiuiu_login
from tuiuiu.tuiuiudocs import admin_urls
from tuiuiu.tuiuiudocs.api.admin.endpoints import DocumentsAdminAPIEndpoint
from tuiuiu.tuiuiudocs.forms import GroupDocumentPermissionFormSet
from tuiuiu.tuiuiudocs.models import get_document_model
from tuiuiu.tuiuiudocs.permissions import permission_policy
from tuiuiu.tuiuiudocs.rich_text import DocumentLinkHandler


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^documents/', include(admin_urls, app_name='tuiuiudocs', namespace='tuiuiudocs')),
    ]


@hooks.register('construct_admin_api')
def construct_admin_api(router):
    router.register_endpoint('documents', DocumentsAdminAPIEndpoint)


class DocumentsMenuItem(MenuItem):
    def is_shown(self, request):
        return permission_policy.user_has_any_permission(
            request.user, ['add', 'change', 'delete']
        )


@hooks.register('register_admin_menu_item')
def register_documents_menu_item():
    return DocumentsMenuItem(
        _('Documents'),
        urlresolvers.reverse('tuiuiudocs:index'),
        name='documents',
        classnames='icon icon-doc-full-inverse',
        order=400
    )


@hooks.register('insert_editor_js')
def editor_js():
    js_files = [
        static('tuiuiudocs/js/hallo-plugins/hallo-tuiuiudoclink.js'),
        static('tuiuiudocs/js/document-chooser.js'),
    ]
    js_includes = format_html_join(
        '\n', '<script src="{0}"></script>',
        ((filename, ) for filename in js_files)
    )
    return js_includes + format_html(
        """
        <script>
            window.chooserUrls.documentChooser = '{0}';
            registerHalloPlugin('hallotuiuiudoclink');
        </script>
        """,
        urlresolvers.reverse('tuiuiudocs:chooser')
    )


@hooks.register('register_rich_text_link_handler')
def register_document_link_handler():
    return ('document', DocumentLinkHandler)


class DocumentsSummaryItem(SummaryItem):
    order = 300
    template = 'tuiuiudocs/homepage/site_summary_documents.html'

    def get_context(self):
        return {
            'total_docs': get_document_model().objects.count(),
        }

    def is_shown(self):
        return permission_policy.user_has_any_permission(
            self.request.user, ['add', 'change', 'delete']
        )


@hooks.register('construct_homepage_summary_items')
def add_documents_summary_item(request, items):
    items.append(DocumentsSummaryItem(request))


class DocsSearchArea(SearchArea):
    def is_shown(self, request):
        return permission_policy.user_has_any_permission(
            request.user, ['add', 'change', 'delete']
        )


@hooks.register('register_admin_search_area')
def register_documents_search_area():
    return DocsSearchArea(
        _('Documents'), urlresolvers.reverse('tuiuiudocs:index'),
        name='documents',
        classnames='icon icon-doc-full-inverse',
        order=400)


@hooks.register('register_group_permission_panel')
def register_document_permissions_panel():
    return GroupDocumentPermissionFormSet


@hooks.register('describe_collection_contents')
def describe_collection_docs(collection):
    docs_count = get_document_model().objects.filter(collection=collection).count()
    if docs_count:
        url = urlresolvers.reverse('tuiuiudocs:index') + ('?collection_id=%d' % collection.id)
        return {
            'count': docs_count,
            'count_text': ungettext(
                "%(count)s document",
                "%(count)s documents",
                docs_count
            ) % {'count': docs_count},
            'url': url,
        }


@hooks.register('before_serve_document')
def check_view_restrictions(document, request):
    """
    Check whether there are any view restrictions on this document which are
    not fulfilled by the given request object. If there are, return an
    HttpResponse that will notify the user of that restriction (and possibly
    include a password / login form that will allow them to proceed). If
    there are no such restrictions, return None
    """
    for restriction in document.collection.get_view_restrictions():
        if not restriction.accept_request(request):
            if restriction.restriction_type == BaseViewRestriction.PASSWORD:
                from tuiuiu.tuiuiucore.forms import PasswordViewRestrictionForm
                form = PasswordViewRestrictionForm(instance=restriction,
                                                   initial={'return_url': request.get_full_path()})
                action_url = urlresolvers.reverse('tuiuiudocs_authenticate_with_password', args=[restriction.id])

                password_required_template = getattr(settings, 'DOCUMENT_PASSWORD_REQUIRED_TEMPLATE', 'tuiuiudocs/password_required.html')

                context = {
                    'form': form,
                    'action_url': action_url
                }
                return TemplateResponse(request, password_required_template, context)

            elif restriction.restriction_type in [BaseViewRestriction.LOGIN, BaseViewRestriction.GROUPS]:
                return require_tuiuiu_login(next=request.get_full_path())
