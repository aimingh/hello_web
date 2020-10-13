from django.shortcuts import render, redirect
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
        data['page_obj'] = result
    return render(request, 'board/listofworknet.html', context=data)

def scrapworknet(request):
    # with MongoClient('mongodb://127.0.0.1:27017') as client:
    #     client.mydb.drop_collection('worknet')
    max_page = int(request.GET['max_page'])
    keyword = request.GET['keyword']
    scrapping_worknet(max_page, keyword)
    return redirect('listofworknet_boardv')