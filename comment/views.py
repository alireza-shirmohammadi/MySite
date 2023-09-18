import datetime

from django.shortcuts import render, redirect

from manager.models import Manager
from .models import Comment


def news_cm_add(request, pk):
    if request.method == "POST":
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        day = now.day

        if len(str(day)) == 1:
            day = "0" + str(day)
        if len(str(month)) == 1:
            month = "0" + str(month)

        today = str(year) + "/" + str(month) + "/" + str(day)
        time = str(now.hour) + ":" + str(now.minute)

        msg = request.POST.get("msg")
        if request.user.is_authenticated:
            manager = Manager.objects.get(utext=request.user)
            cm = Comment(
                cm=msg,
                name=manager.utext,
                email=manager.email,
                news_id=pk,
                date=today,
                time=time,
            )
            cm.save()
        else:
            name = request.POST.get("name")
            email = request.POST.get("email")
            cm = Comment(cm=msg, name=name, email=email, news_id=pk)
            cm.save()
    return redirect("news_detail", pk)


def comments_list(request):
    cm = Comment.objects.all().order_by("-pk")
    return render(request, "back/comments_list.html", {"cm": cm})


def comments_del(request, pk):
    cm = Comment.objects.filter(pk=pk)
    cm.delete()
    return redirect("comments_list")


def comments_confirme(request, pk):
    cm = Comment.objects.get(pk=pk)
    cm.status = 1
    cm.save()
    return redirect("comments_list")


def comments_unconfirme(request, pk):
    cm = Comment.objects.get(pk=pk)
    cm.status = 0
    cm.save()
    return redirect("comments_list")
