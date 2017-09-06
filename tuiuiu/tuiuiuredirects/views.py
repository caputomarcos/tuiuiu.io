from __future__ import absolute_import, unicode_literals

from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _
from django.views.decorators.vary import vary_on_headers

from tuiuiu.utils.pagination import paginate
from tuiuiu.tuiuiuadmin import messages
from tuiuiu.tuiuiuadmin.forms import SearchForm
from tuiuiu.tuiuiuadmin.utils import PermissionPolicyChecker, permission_denied
from tuiuiu.tuiuiuredirects import models
from tuiuiu.tuiuiuredirects.forms import RedirectForm
from tuiuiu.tuiuiuredirects.permissions import permission_policy

permission_checker = PermissionPolicyChecker(permission_policy)


@permission_checker.require_any('add', 'change', 'delete')
@vary_on_headers('X-Requested-With')
def index(request):
    query_string = request.GET.get('q', "")
    ordering = request.GET.get('ordering', 'old_path')

    redirects = models.Redirect.objects.prefetch_related('redirect_page', 'site')

    # Search
    if query_string:
        redirects = redirects.filter(old_path__icontains=query_string)

    # Ordering (A bit useless at the moment as only 'old_path' is allowed)
    if ordering not in ['old_path']:
        ordering = 'old_path'

    redirects = redirects.order_by(ordering)

    # Pagination
    paginator, redirects = paginate(request, redirects)

    # Render template
    if request.is_ajax():
        return render(request, "tuiuiuredirects/results.html", {
            'ordering': ordering,
            'redirects': redirects,
            'query_string': query_string,
        })
    else:
        return render(request, "tuiuiuredirects/index.html", {
            'ordering': ordering,
            'redirects': redirects,
            'query_string': query_string,
            'search_form': SearchForm(
                data=dict(q=query_string) if query_string else None, placeholder=_("Search redirects")
            ),
            'user_can_add': permission_policy.user_has_permission(request.user, 'add'),
        })


@permission_checker.require('change')
def edit(request, redirect_id):
    theredirect = get_object_or_404(models.Redirect, id=redirect_id)

    if not permission_policy.user_has_permission_for_instance(
        request.user, 'change', theredirect
    ):
        return permission_denied(request)

    if request.method == 'POST':
        form = RedirectForm(request.POST, request.FILES, instance=theredirect)
        if form.is_valid():
            form.save()
            messages.success(request, _("Redirect '{0}' updated.").format(theredirect.title), buttons=[
                messages.button(reverse('tuiuiuredirects:edit', args=(theredirect.id,)), _('Edit'))
            ])
            return redirect('tuiuiuredirects:index')
        else:
            messages.error(request, _("The redirect could not be saved due to errors."))
    else:
        form = RedirectForm(instance=theredirect)

    return render(request, "tuiuiuredirects/edit.html", {
        'redirect': theredirect,
        'form': form,
        'user_can_delete': permission_policy.user_has_permission(request.user, 'delete'),
    })


@permission_checker.require('delete')
def delete(request, redirect_id):
    theredirect = get_object_or_404(models.Redirect, id=redirect_id)

    if not permission_policy.user_has_permission_for_instance(
        request.user, 'delete', theredirect
    ):
        return permission_denied(request)

    if request.method == 'POST':
        theredirect.delete()
        messages.success(request, _("Redirect '{0}' deleted.").format(theredirect.title))
        return redirect('tuiuiuredirects:index')

    return render(request, "tuiuiuredirects/confirm_delete.html", {
        'redirect': theredirect,
    })


@permission_checker.require('add')
def add(request):
    if request.method == 'POST':
        form = RedirectForm(request.POST, request.FILES)
        if form.is_valid():
            theredirect = form.save()

            messages.success(request, _("Redirect '{0}' added.").format(theredirect.title), buttons=[
                messages.button(reverse('tuiuiuredirects:edit', args=(theredirect.id,)), _('Edit'))
            ])
            return redirect('tuiuiuredirects:index')
        else:
            messages.error(request, _("The redirect could not be created due to errors."))
    else:
        form = RedirectForm()

    return render(request, "tuiuiuredirects/add.html", {
        'form': form,
    })
