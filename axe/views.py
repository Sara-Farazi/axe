import re

from django.http import HttpResponse
from django.shortcuts import render
from axe.data_provider import get_keyword_results

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words("english"))

PAGE_SIZE = 16


def get_keywords(query):
    tokens = []
    for token in word_tokenize(query):
        if token not in stop_words and token.isalnum():
            tokens.append(token)

    return tokens


def is_search_request(request):
    return not request.GET == {}


def validate_advanced_search(query, max_size, min_size):
    if query == "" and min_size == "" and max_size == "":
        return False

    if min_size != "" and not min_size.isdecimal():
        return False

    if max_size != "" and not max_size.isdecimal():
        return False

    return True


def get_results_page(results, page):
    page_index = page - 1
    return results[page_index*PAGE_SIZE:page_index*PAGE_SIZE+PAGE_SIZE]


def index(request):
    if request.method == 'GET':

        if not is_search_request(request):
            return render(request, 'index.html')

        query = request.GET['query']
        min_size = request.GET['min_size']
        max_size = request.GET['max_size']

        if not validate_advanced_search(query, max_size, min_size):
            return render(request, 'index.html', {
                'advanced_search_error': True
            })

        keywords = get_keywords(query)
        results = [result.decode("utf-8") for result in get_keyword_results(keywords)]

        try:
            page = int(request.GET['page'])
        except Exception:
            page = 1

        return render(request, 'results.html', {
            "results": get_results_page(results, page)
        })

    else:
        return HttpResponse("Invalid request")


def search_results(request):
    if request.method == 'GET':
        return render(request, 'results.html')
