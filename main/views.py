from django.shortcuts import render,redirect
from .models import Main
from news.models import News
from subcat.models import SubCat
from cat.models import Cat
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
# Create your views here.
def home (request):
    site=Main.objects.get(pk=1)
    news=News.objects.all().order_by('-pk')
    cat=Cat.objects.all()
    subcat=SubCat.objects.all()
    lastnews=News.objects.all().order_by('-pk')[:3]
    popnews= News.objects.all().order_by('-show')
    popnews2 = News.objects.all().order_by('-show')[:3]
    return render(request,'front/home.html',{'site':site,'news':news,'cat':cat,'subcat':subcat,'lastnews':lastnews,'popnews2':popnews2,'popnews':popnews})
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

def site_setting(request):
 # login check start
    if not request.user.is_authenticated :
        return redirect('mylogin')
    # login check end


    if request.method == 'POST' :

        name = request.POST.get('name')
        tell = request.POST.get('tell')
        fb = request.POST.get('fb')
        tw = request.POST.get('tw')
        yt = request.POST.get('yt')
        link = request.POST.get('link')
        txt = request.POST.get('txt')

        if fb == "" : fb = "#"
        if tw == "" : tw = "#"
        if yt == "" : yt = "#"
        if link == "" : link = "#"

        if name == "" or tell == "" or txt == "" :
            error = "All Fields Requirded"
            return render(request, 'back/error.html' , {'error':error})

        try :

            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)

            picurl = url
            picname = filename

        except :

            picurl = "-"
            picname = "-"



        try :

            myfile2 = request.FILES['myfile2']
            fs2 = FileSystemStorage()
            filename2 = fs2.save(myfile2.name, myfile2)
            url2 = fs2.url(filename2)

            picurl2 = url2
            picname2 = filename2

        except :

            picurl2 = "-"
            picname2 = "-"



        b = Main.objects.get(pk=1)
        b.name = name
        b.tell = tell
        b.fb = fb
        b.tw = tw
        b.yt = yt
        b.link = link
        b.about = txt

        if picurl != "-" : b.picurl = picurl
        if picname != "-" : b.picname = picname
        if picurl2 != "-" :  b.picurl2 = picurl2
        if picname2 != "-" : b.picname2 = picname2

        b.save()





    site = Main.objects.get(pk=1)


    return render(request, 'back/setting.html', {'site':site})
