from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def hello(request):
    return HttpResponse("<h1>Hello Django</h1><p>content...</p>")


def responsewithhtml(request):
    data = {
        'first': 'Junhee',
        'second': 'Cho'
    }
    return render(request, 'home/responsewithhtml.html', context=data)
