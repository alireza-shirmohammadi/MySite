from django.shortcuts import render, redirect

from .models import Trending


def trending_add(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect("mylogin")
    # login check end
    if request.method == "POST":
        txt = request.POST.get("txt")
        if txt == "":
            error = "All Fields Requirded"
            return render(request, "back/error.html", {"error": error})
        b = Trending(txt=txt)
        b.save()
    trendinglist = Trending.objects.all()
    return render(request, "back/trending.html", {"trendinglist": trendinglist})


def trending_del(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect("mylogin")
    # login check end
    b = Trending.objects.filter(pk=pk)
    b.delete()
    return redirect("trending_add")


def trending_edit(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect("mylogin")
    # login check end
    mytxt = Trending.objects.get(pk=pk).txt
    if request.method == "POST":
        txt = request.POST.get("txt")
        if txt == "":
            error = "All Fields Requirded"
            return render(request, "back/error.html", {"error": error})
        b = Trending.objects.get(pk=pk)
        b.txt = txt
        b.save()
        return redirect("trending_add")
    return render(request, "back/trending_edit.html", {"mytxt": mytxt, "pk": pk})
