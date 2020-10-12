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

def organization(request):
    data = {
        'name': 'Junhee Cho',
        'Tel': '010-000-0000',
        'address': 'Seoul, Republic of korea'
    }
    return render(request, 'home/organization.html', context=data)