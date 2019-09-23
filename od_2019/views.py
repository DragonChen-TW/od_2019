from django.shortcuts import HttpResponse

def index(request):
    return HttpResponse('<a href="/house/"><h3>Main House Page</h3></a>')
