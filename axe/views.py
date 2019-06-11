import os
import time
import uuid
import math
import zipfile


from django.http import HttpResponse
from django.shortcuts import render
from axe.data_provider import get_query_results

PAGE_SIZE = 16


QUERY_PROCESSING_TIME_HISTORY = []


def record_query_processing_time(func):
    def wrapper(*args, **kwargs):
        request = list(args)[0]
        start_time = time.time()
        response = func(*args, **kwargs)
        processing_time = time.time() - start_time

        if is_search_request(request):
            QUERY_PROCESSING_TIME_HISTORY.append({
                "query": request.GET['query'],
                "min_size": request.GET['min_size'],
                "max_size": request.GET['max_size'],
                "processing_time": processing_time,
                "timestamp": start_time
            })
        return response

    return wrapper


def compress_images(images):
    image_files = [{
        "filepath": os.getcwd() + '/data/images/{}.jpg'.format(image),
        "filename": "{}.jpg".format(image)
    } for image in images]
    path = os.getcwd() + "/data/downloads/"
    compressed_file_path = path + "{}.zip".format(uuid.uuid4().__str__())
    with zipfile.ZipFile(compressed_file_path, 'w') as image_archive:
        for f in image_files:
            image_archive.write(f["filepath"], f["filename"])

    return compressed_file_path


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
        "next": next_page,
        "total": pages
    }


def is_search_request(request):
    return not request.GET == {}


def validate_search(query, max_size, min_size):
    if query == "":
        return False

    if min_size != "" and not min_size.isdecimal():
        return False

    if max_size != "" and not max_size.isdecimal():
        return False

    return True


def get_results_page(results, page):
    page_index = page - 1
    return results[page_index * PAGE_SIZE:page_index * PAGE_SIZE + PAGE_SIZE]


@record_query_processing_time
def index(request):
    if request.method == 'GET':

        if not is_search_request(request):
            return render(request, 'index.html')

        query = request.GET['query']
        min_size = request.GET['min_size']
        max_size = request.GET['max_size']

        if not validate_search(query, max_size, min_size):
            return render(request, 'index.html', {
                'search_error': True
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


def download(request):
    try:
        images = request.GET['images'].split(",")
        compressed_file_path = compress_images(images)

        with open(compressed_file_path, 'rb') as zf:
            response = HttpResponse(zf.read(), content_type="application/zip")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(compressed_file_path)
            return response

    except Exception as e:
        return None


def get_query_history(request):
    return render(request, 'queries.html', {
        "queries": QUERY_PROCESSING_TIME_HISTORY
    })
