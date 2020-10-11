from django.shortcuts import render,redirect
from .models import Main
from news.models import News
from subcat.models import SubCat
from cat.models import Cat
from django.contrib.auth import authenticate, login, logout
# Create your views here.
def home (request):
    site=Main.objects.get(pk=1)
    news=News.objects.all().order_by('-pk')
    cat=Cat.objects.all()
    subcat=SubCat.objects.all()
    lastnews=News.objects.all().order_by('-pk')[:3]
    return render(request,'front/home.html',{'site':site,'news':news,'cat':cat,'subcat':subcat,'lastnews':lastnews})
def about (request):
    site=Main.objects.get(pk=1)
    return render(request,'front/about.html',{'site':site})
def panel (request):
      # login check start
    if not request.user.is_authenticated :
        return redirect('mylogin')
    # login check end
    return render (request,'back/home.html')
def mylogin (request):
    if request.method == 'POST' :

        utxt = request.POST.get('username')
        ptxt = request.POST.get('password')

        if utxt != "" and ptxt != "" :

            user = authenticate(username=utxt, password=ptxt)
            if user !=None:
                login(request,user)
                return redirect('panel')

    return render(request,'front/mylogin.html')
def mylogout (request):
    logout(request)
    return redirect('mylogin')
