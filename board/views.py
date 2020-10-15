from django.shortcuts import render, redirect
from pymongo import MongoClient
from datas.scraping_jobsearch import scrapping_jobkorea, scrapping_worknet
from django.core.paginator import Paginator

def listwithmongo(request):
    data = request.GET.copy()
    with MongoClient('mongodb://127.0.0.1:27017') as client:
        mydb = client.mydb
        result = list(mydb.economic.find({}))
        data['page_obj'] = result
    return render(request, 'board/listwithmongo.html', context=data)

def listwithmongowithpaginator(request):
    data = request.GET.copy()
    with MongoClient('mongodb://127.0.0.1:27017') as client:
        mydb = client.mydb
        contact_list = list(mydb.economic.find({}))
    paginator = Paginator(contact_list, 10)
    page_number = request.GET.get('page', 1)
    data['page_obj'] = paginator.get_page(page_number)
    return render(request, 'board/listwithmongowithpaginator.html', context=data)

# 페이징 처리를 위해 페이지네이터 사용
def paging(request, datalist, num=10):
    page = request.GET.get('page', '1')
    paginator = Paginator(datalist, num)
    page_obj = paginator.get_page(page)
    page = int(page)
    maxpage = num*((page-1)//num)+10
    minpage = num*((page-1)//num)+1
    return page_obj, maxpage, minpage

def listofworknet(request):
    data = request.GET.copy()
    with MongoClient('mongodb://127.0.0.1:27017') as client:
        mydb = client.mydb
        result = list(mydb.worknet.find({}))
    page_obj, maxpage, minpage = paging(request, result)
    data['page_obj'] = page_obj
    data['maxpage'] = maxpage
    data['minpage'] = minpage
    return render(request, 'board/listofworknet.html', context=data)

def scrapworknet(request):
    # with MongoClient('mongodb://127.0.0.1:27017') as client:
    #     client.mydb.drop_collection('worknet')
    max_page = int(request.GET['max_page'])
    keyword = request.GET['keyword']
    scrapping_worknet(max_page, keyword)
    return redirect('listofworknet_boardv')

def listofjobkorea(request):
    data = request.GET.copy()
    with MongoClient('mongodb://127.0.0.1:27017') as client:
        mydb = client.mydb
        result = list(mydb.jobkorea.find({}))
    page_obj, maxpage, minpage = paging(request, result)
    data['page_obj'] = page_obj
    data['maxpage'] = maxpage
    data['minpage'] = minpage
    return render(request, 'board/listofjobkorea.html', context=data)

def scrapjobkorea(request):
    # with MongoClient('mongodb://127.0.0.1:27017') as client:
    #     client.mydb.drop_collection('jobkorea')
    max_page = int(request.GET['max_page'])
    keyword = request.GET['keyword']
    scrapping_jobkorea(max_page, keyword)
    return redirect('listofjobkorea_boardv')