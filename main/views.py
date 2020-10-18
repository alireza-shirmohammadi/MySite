from django.shortcuts import render,redirect
from .models import Main
from news.models import News
from subcat.models import SubCat
from trending.models import Trending
from cat.models import Cat
from manager.models import Manager
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
# Create your views here.
def home (request):
    site=Main.objects.get(pk=1)
    news=News.objects.all().order_by('-pk')
    cat=Cat.objects.all()
    subcat=SubCat.objects.all()
    lastnews=News.objects.all().order_by('-pk')[:3]
    popnews= News.objects.all().order_by('-show')
    popnews2 = News.objects.all().order_by('-show')[:3]
    trending=Trending.objects.all().order_by('-pk')[:5]
    return render(request,'front/home.html',{'site':site,'news':news,'cat':cat,'subcat':subcat,'lastnews':lastnews,'popnews2':popnews2,'popnews':popnews,'trending':trending})
def about (request):
    site=Main.objects.get(pk=1)
    news=News.objects.all().order_by('-pk')
    cat=Cat.objects.all()
    subcat=SubCat.objects.all()
    lastnews=News.objects.all().order_by('-pk')[:3]
    popnews= News.objects.all().order_by('-show')
    popnews2 = News.objects.all().order_by('-show')[:3]
    trending=Trending.objects.all().order_by('-pk')[:5]
    return render(request,'front/about.html',{'site':site,'news':news,'cat':cat,'subcat':subcat,'lastnews':lastnews,'popnews2':popnews2,'popnews':popnews,'trending':trending})
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
def about_setting (request):
    # login check start
    if not request.user.is_authenticated :
        return redirect('mylogin')
       # login check end


    if request.method == 'POST' :
        txt=request.POST.get('txt')
        if txt == "" :
            error = "All Fields Requirded"
            return render(request, 'back/error.html' , {'error':error})

        b = Main.objects.get(pk=1)
        b.abouttxt = txt
        b.save()

    about = Main.objects.get(pk=1).abouttxt
    return render (request,'back/about_setting.html',{'about':about})

def contact (request):
    trending=Trending.objects.all().order_by('-pk')[:5]
    site = Main.objects.get(pk=2)
    news = News.objects.all().order_by('-pk')
    cat = Cat.objects.all()
    subcat = SubCat.objects.all()
    lastnews = News.objects.all().order_by('-pk')[:3]
    popnews2 = News.objects.all().order_by('-show')[:3]


    return render(request, 'front/contact.html' , {'site':site, 'news':news, 'cat':cat, 'subcat':subcat, 'lastnews':lastnews, 'popnews2':popnews2,'trending':trending})

def change_pass(request):

    # login check start
    if not request.user.is_authenticated :
        return redirect('mylogin')
    # login check end

    if request.method == 'POST' :

        oldpass = request.POST.get('oldpass')
        newpass = request.POST.get('newpass')

        if oldpass == "" or newpass == "" :
            error = "All Fields Requirded"
            return render(request, 'back/error.html' , {'error':error})

        user = authenticate(username=request.user, password=oldpass)

        if user != None :

            if len(newpass) < 8 :
                error = "Your Password Most Be At Less 8 Character"
                return render(request, 'back/error.html' , {'error':error})

            count1 = 0
            count2 = 0


            for i in newpass :

                if i > "0" and i < "9" :
                    count1 = 1
                if (i > "A" and i < "Z") or ( i > 'a' and i < 'z')  :
                    count2 = 1



            if count1 == 1 and count2 == 1 :

                user = User.objects.get(username=request.user)
                user.set_password(newpass)
                user.save()
                return redirect('mylogout')
            else:
                error = "Your Password Is Not strong enough"
                return render(request, 'back/error.html' , {'error':error})
        else:

            error = "Your Password Is Not Correct"
            return render(request, 'back/error.html' , {'error':error})


    return render(request, 'back/changepass.html')

def myregister (request):
    if request.method == 'POST':
        name=request.POST.get('name')
        lastname=request.POST.get('lastname')
        email=request.POST.get('email')
        utext=request.POST.get('utext')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
        if pass1 != pass2 :
            msg = "Your Pass Didn't Match"
            return render(request, 'front/msgbox.html', {'msg':msg})
        count1 = 0
        count2 = 0
        #count3 = 0
        #count4 = 0

        for i in pass1 :

            if i > "0" and i < "9" :
                count1 = 1
            if (i > "A" and i < "Z") or ( i > 'a' and i < 'z')  :
                count2 = 1

            #if i > "!" and i < "(" :
                #count4 = 1

        if count1 == 0 or count2 == 0 :
            msg = "Your Pass Is Not Strong"
            return render(request, 'front/msgbox.html', {'msg':msg})

        if len(pass1) < 8 :
            msg = "Your Pass Most Be 8 Character"
            return render(request, 'front/msgbox.html', {'msg':msg})
        if len(User.objects.filter(username=utext)) == 0 and len(User.objects.filter(email=email)) == 0 :
            user=User.objects.create_user(username=utext,password=pass1,email=email)
            b=Manager(name=name,lastname=lastname,email=email,utext=utext)
            b.save()
            user1 = authenticate(username=utext, password=pass1)
            if user1 !=None:
                login(request,user1)
                return redirect('home')
        else :
            msg = "this username or email is already exist"
            return render(request, 'front/msgbox.html', {'msg':msg})
    return render (request,'front/mylogin.html')
