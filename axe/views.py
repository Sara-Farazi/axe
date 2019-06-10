import math
import sqlite3

from django.http import HttpResponse
from django.shortcuts import render
from axe.data_provider import get_query_results

PAGE_SIZE = 16


def get_pagination_items(results_size, page):
    pages = math.ceil(results_size / PAGE_SIZE)
    next_page = page + 1
    prev_page = page - 1

    if page == 1:
        prev_page = "disabled"

    if page == pages:
        next_page = "disabled"

    return {
        "page": page,
        "prev": prev_page,
        "next": next_page
    }


def is_search_request(request):
    return not request.GET == {}


def validate_search(query, max_size, min_size):
    if query == "" and min_size == "" and max_size == "":
        return False

    if min_size != "" and not min_size.isdecimal():
        return False

    if max_size != "" and not max_size.isdecimal():
        return False

    return True


def get_results_page(results, page):
    page_index = page - 1
    return results[page_index * PAGE_SIZE:page_index * PAGE_SIZE + PAGE_SIZE]


def index(request):
    if request.method == 'GET':

        if not is_search_request(request):
            return render(request, 'index.html')

        query = request.GET['query']
        min_size = request.GET['min_size']
        max_size = request.GET['max_size']

        if not validate_search(query, max_size, min_size):
            return render(request, 'index.html', {
                'advanced_search_error': True
            })

        results = [result.decode("utf-8") for result in get_query_results(query, min_size, max_size)]

        try:
            page = int(request.GET['page'])
        except Exception:
            page = 1

        return render(request, 'results.html', {
            "results": get_results_page(results, page),
            "pages": get_pagination_items(len(results), page)
        })

    else:
        return HttpResponse("Invalid request")


def search_results(request):
    if request.method == 'GET':
        return render(request, 'results.html')
