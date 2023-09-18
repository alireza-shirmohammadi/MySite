from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from .models import Newsletter


def news_letter(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect("mylogin")
    # login check end

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":
            perm = 1

    if perm == 0:
        error = "Access Denied"
        return render(request, "back/error.html", {"error": error})

    if request.method == "POST":
        txt = request.POST.get("txt")
        if txt != "":
            b = Newsletter(txt=txt)
            b.save()

    return redirect("home")


def news_email(request):
    # login check start
    if not request.user.is_authenticated:
        return redirect("mylogin")
    # login check end

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":
            perm = 1

    if perm == 0:
        error = "Access Denied"
        return render(request, "back/error.html", {"error": error})

    email = Newsletter.objects.all()
    return render(request, "back/email.html", {"email": email})


def news_txt_del(request, pk):
    # login check start
    if not request.user.is_authenticated:
        return redirect("mylogin")
    # login check end

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser":
            perm = 1

    if perm == 0:
        error = "Access Denied"
        return render(request, "back/error.html", {"error": error})

    b = Newsletter.objects.filter(pk=pk)
    b.delete()
    return redirect("news_email")


def news_letter_ans(request):
    if request.method == "POST":
        txt = request.POST.get("txt")
        a = []
        for i in Newsletter.objects.all():
            a.append(Newsletter.objects.get(pk=i.pk).txt)

        subject = "answer"
        message = txt
        email_from = settings.EMAIL_HOST_USER
        emails = a
        send_mail(subject, message, email_from, emails)

        return redirect("news_email")
