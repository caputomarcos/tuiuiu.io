from __future__ import absolute_import, unicode_literals

from django.shortcuts import render

from tuiuiu.utils.pagination import paginate
from tuiuiu.tuiuiuadmin.forms import SearchForm
from tuiuiu.tuiuiuadmin.modal_workflow import render_modal_workflow
from tuiuiu.tuiuiusearch import models
from tuiuiu.tuiuiusearch.utils import normalise_query_string


def chooser(request, get_results=False):
    # Get most popular queries
    queries = models.Query.get_most_popular()

    # If searching, filter results by query string
    query_string = None
    if 'q' in request.GET:
        searchform = SearchForm(request.GET)
        if searchform.is_valid():
            query_string = searchform.cleaned_data['q']
            queries = queries.filter(query_string__icontains=normalise_query_string(query_string))
    else:
        searchform = SearchForm()

    paginator, queries = paginate(request, queries, per_page=10)

    # Render
    if get_results:
        return render(request, "tuiuiusearch/queries/chooser/results.html", {
            'queries': queries,
        })
    else:
        return render_modal_workflow(
            request, 'tuiuiusearch/queries/chooser/chooser.html', 'tuiuiusearch/queries/chooser/chooser.js', {
                'queries': queries,
                'searchform': searchform,
            }
        )


def chooserresults(request):
    return chooser(request, get_results=True)
