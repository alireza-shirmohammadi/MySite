from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render

from cat.models import Cat
from main.models import Main
from news.models import News
from subcat.models import SubCat
from trending.models import Trending

mysearch = None


def search_db(search_text):
    return News.objects.filter(name__icontains=search_text).order_by("-show")[:5]


def search(request):
    site = Main.objects.get(pk=1)
    news = News.objects.filter(act=1).order_by("-pk")
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.filter(act=1).order_by("-pk")[:3]
    popnews = News.objects.filter(act=1).order_by("-show")
    popnews2 = News.objects.filter(act=1).order_by("-show")[:3]
    trending = Trending.objects.all().order_by("-pk")[:5]
    lastnews2 = News.objects.filter(act=1).order_by("-pk")[:4]
    global mysearch

    if request.method == "POST":
        q = request.POST.get("search")
        mysearch = q
        response = search_db(q) if q else ""
    else:
        response = search_db(mysearch) if mysearch else ""
    paginator = Paginator(response, 9)
    page = request.GET.get("page")
    try:
        searchnews = paginator.page(page)
    except EmptyPage:
        searchnews = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        searchnews = paginator.page(1)

    return render(
        request,
        "front/search_news.html",
        {
            "searchnews": searchnews,
            "lastnews2": lastnews2,
            "site": site,
            "news": news,
            "cat": cat,
            "subcat": subcat,
            "lastnews": lastnews,
            "popnews2": popnews2,
            "popnews": popnews,
            "trending": trending,
        },
    )
def search_api(request):
    if not request.is_ajax():
        return JsonResponse({})
    search_text = request.POST.get("search_text")
    response = search_db(search_text)
    if len(response) > 0 and len(search_text) > 0:
        data = []
        for item in response:
            dic = {
                "id": item.id,
                "name": item.name,
                "img": item.picurl,
                "date": item.date,
            }
            data.append(dic)
        res = data
    else:
        res = "No reasult found!!!"

    return JsonResponse({"data": res})
