from django.shortcuts import render
from news.models import News
from .documents import NewsDocument
from main.models import Main
from subcat.models import SubCat
from cat.models import Cat
from trending.models import Trending
from elasticsearch_dsl.query import MoreLikeThis
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

mysearch=None


def search(request):
    site = Main.objects.get(pk=1)
    news = News.objects.filter(act=1).order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.filter(act=1).order_by('-pk')[:3]
    popnews = News.objects.filter(act=1).order_by('-show')
    popnews2 = News.objects.filter(act=1).order_by('-show')[:3]
    trending = Trending.objects.all().order_by('-pk')[:5]
    lastnews2 = News.objects.filter(act=1).order_by('-pk')[:4]
    allnews = News.objects.all()
    global mysearch

    if request.method=='POST':

        q=request.POST.get('search')
        mysearch=q
        #print(mysearch)
        if q:
            searchnewss= NewsDocument.search().filter('prefix',name=q)
            response = searchnewss.execute()
           # print(response[0].name)

        else:
            searchnewss= ''
            response = ''
    else:

        if mysearch:
            #print(mysearch)
            searchnewss= NewsDocument.search().filter('prefix',name=mysearch)
            response = searchnewss.execute()
            #print(mysearch)
        else:
           # print(mysearch)
            searchnewss= ''
            response = ''

    paginator = Paginator(response, 9)
    page = request.GET.get('page')
    try:
        searchnews = paginator.page(page)
    except EmptyPage:
        searchnews = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        searchnews = paginator.page(1)

    return render(request , 'front/search_news.html' ,{'searchnews':searchnews,'lastnews2':lastnews2,'site':site,
    'news':news,'cat':cat,'subcat':subcat,'lastnews':lastnews,'popnews2':popnews2,'popnews':popnews,'trending':trending})




'''   
        search=request.POST.get('search')
        mysearch=search
        a=News.objects.filter(name__contains=search)
        b=News.objects.filter(short_txt__contains=search)
        c=News.objects.filter(body_txt__contains=search)
        searchnewss=list(chain(a,b,c))
        searchnewss=list(dict.fromkeys(searchnewss))
    else:
        print(mysearch)
        a=News.objects.filter(name__contains=mysearch)
        b=News.objects.filter(short_txt__contains=mysearch)
        c=News.objects.filter(body_txt__contains=mysearch)
        searchnewss=list(chain(a,b,c))
        searchnewss=list(dict.fromkeys(searchnewss))

    site=Main.objects.get(pk=1)
    news=News.objects.filter(act=1).order_by('-pk')
    cat=Cat.objects.all()
    subcat=SubCat.objects.all()
    lastnews=News.objects.filter(act=1).order_by('-pk')[:3]
    popnews= News.objects.filter(act=1).order_by('-show')
    popnews2 = News.objects.filter(act=1).order_by('-show')[:3]
    trending=Trending.objects.all().order_by('-pk')[:5]
    lastnews2=News.objects.filter(act=1).order_by('-pk')[:4]
    allnews=News.objects.all()




    paginator=Paginator(searchnewss,2)
    page=request.GET.get('page')
    try:
        searchnews=paginator.page(page)
    except EmptyPage:
        searchnews=paginator.page(paginator.num_page)
    except PageNotAnInteger:
        searchnews=paginator.page(1)


    return render(request,'front/search_news.html',{'searchnews':searchnews,'lastnews2':lastnews2,'site':site,
    'news':news,'cat':cat,'subcat':subcat,'lastnews':lastnews,'popnews2':popnews2,'popnews':popnews,'trending':trending})
    
    
'''

def search_api(request):
    if request.is_ajax():
        res = None
        search_text=request.POST.get('search_text')
        query=NewsDocument.search().filter('prefix',name=search_text)
        response = query.execute()

        if len(response)>0 and len(search_text) > 0 :
            data=[]
            for item in response:
                dic={
                    'id':item.id,
                    'name':item.name,
                    'img':item.picurl,
                    'date':item.date
                }
                data.append(dic)
            res=data
        else:
            res='No reasult found!!!'

        return JsonResponse({"data": res})
    else:
        return JsonResponse({})