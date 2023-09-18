import datetime

from django.shortcuts import render, redirect

from .models import BlackList


def black_list(request):
    ip = BlackList.objects.all()
    return render(request, "back/blacklist.html", {"ip": ip})


def ip_add(request):
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

        ip = request.POST.get("ip")
        b = BlackList(ip=ip, date=today)
        b.save()
        return redirect("black_list")


def ip_del(request, pk):
    b = BlackList.objects.filter(pk=pk)
    b.delete()
    return redirect("black_list")
