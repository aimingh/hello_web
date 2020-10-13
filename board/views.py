from django.shortcuts import render
from pymongo import MongoClient
from datas.scraping_worknet import scrapping_worknet

def listwithmongo(request):
    data = request.GET.copy()
    with MongoClient('mongodb://127.0.0.1:27017') as client:
        mydb = client.mydb
        result = list(mydb.economic.find({}))
        data['page_obj'] = result
    return render(request, 'board/listwithmongo.html', context=data)

def listofworknet(request):
    data = request.GET.copy()
    with MongoClient('mongodb://127.0.0.1:27017') as client:
        mydb = client.mydb
        result = list(mydb.worknet.find({}))
        if len(result)==0:
            scrapping_worknet(10)
            result = list(mydb.worknet.find({}))
        data['page_obj'] = result
    return render(request, 'board/listofworknet.html', context=data)