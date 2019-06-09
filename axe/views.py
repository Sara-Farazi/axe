from django.shortcuts import render


# Create your views here.
def index(request):
    if request.method == 'POST':
        if 'text_search' in request.POST:
            text = request.POST['text']
            if text == "":
                return render(request, 'index.html', {
                    'alerts': True
                })
            return render(request, 'results.html')
        elif 'advanced_search' in request.POST:
            keywords = request.POST['keywords']
            min_size = request.POST['min_size']
            max_size = request.POST['max_size']
            if keywords == "" and min_size == "" and max_size == "":
                return render(request, 'index.html', {
                    'alerts': True
                })             
            return render(request, 'results.html')
        else:
            return render(request, 'index.html')

    else:
        return render(request, 'index.html')


def search_results(request):
    if request.method == 'GET':
        return render(request, 'results.html')

