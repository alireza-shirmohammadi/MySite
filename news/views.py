from django.shortcuts import render,redirect
from .models import News
from main.models import Main
from django.core.files.storage import FileSystemStorage
import datetime
from subcat.models import SubCat
from cat.models import Cat
from trending.models import Trending
from django.contrib.auth.models import User,Group,Permission
from comment.models import Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
#from .crawler import Crawler
import csv

from itertools import chain


# Create your views here.

def news_detail(request,pk):
    shownews=News.objects.filter(pk=pk)
    site=Main.objects.get(pk=1)
    news=News.objects.filter(act=1).order_by('-pk')
    cat=Cat.objects.all()
    subcat=SubCat.objects.all()
    lastnews=News.objects.filter(act=1).order_by('-pk')[:3]
    popnews= News.objects.filter(act=1).order_by('-show')
    popnews2 = News.objects.filter(act=1).order_by('-show')[:3]
    tagname = News.objects.get(pk=pk).tag
    trending=Trending.objects.all().order_by('-pk')[:5]
    tag = tagname.split(',')
    code=News.objects.get(pk=pk).pk
    comment=Comment.objects.filter(news_id=code,status=1).order_by('-pk')
    cmcount=Comment.objects.filter(news_id=code,status=1).count()
    link="/news/" + str(News.objects.get(pk=pk).pk)
    print(cmcount)
    try:

        mynews = News.objects.get(pk=pk)
        mynews.show = mynews.show + 1
        mynews.save()

    except:

        print("Can't Add Show")
    return render(request,'front/news_detail.html',{'link':link,'comment':comment,'cmcount':cmcount,'code':code,'site':site,'trending':trending,'news':news,'cat':cat,'subcat':subcat,'lastnews':lastnews,'shownews':shownews,'popnews':popnews,'popnews2':popnews2,'tag':tag})

def news_list(request):
      # login check start
    if not request.user.is_authenticated :
        return redirect('mylogin')
    # login check end
    perm=0
    for i in request.user.groups.all():
        if i.name=='masteruser':perm=1
    if perm==1 :
        newss=News.objects.all()
        # paginator=Paginator(newss,2)
        # page=request.GET.get('page')
        # try:
        #     news=paginator.page(page)
        # except EmptyPage:
        #     news=paginator.page(paginator.num_page)
        # except PageNotAnInteger:
        #     news=paginator.page(1)
    else:
        newss=News.objects.filter(writer=request.user)
    return render(request,'back/news_list.html',{'news':newss})
def news_add(request):
      # login check start
    if not request.user.is_authenticated :
        return redirect('mylogin')
    # login check end
    cat=News.objects.all()
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day

    if len(str(day)) == 1 :
        day = "0" + str(day)
    if len(str(month)) == 1 :
        month = "0" + str(month)


    today = str(year) + "/" + str(month) + "/" + str(day)
    time = str(now.hour) + ":" + str(now.minute)

    date = str(year) + str(month) + str(day)
    cat = SubCat.objects.all()
    if request.method=='POST':
        newstitle=request.POST.get('newstitle')
        newscat=request.POST.get('newscat')
        newstxtshort=request.POST.get('newstxtshort')
        newstxt=request.POST.get('newstxt')
        catid = request.POST.get('newscat')
        tag=request.POST.get('tag')
        if newstitle=='' or newscat== '' or newstxtshort=='' or newstxt=='' or newscat == "" :
            error= "All Fields Requirded"
            return render (request,'back/error.html',{'error':error})

        try:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)

            if str(myfile.content_type).startswith("image"):

                if myfile.size < 5000000 :

                    newsname = SubCat.objects.get(pk=catid).name
                    ocatid = SubCat.objects.get(pk=catid).catid

                    b = News(name=newstitle, short_txt=newstxtshort, body_txt=newstxt, date=today, picname=filename, picurl=url, writer=request.user, catname=newsname, catid=catid,tag=tag, show=0, time=time, ocatid=ocatid,)
                    b.save()

                    count = len(News.objects.filter(ocatid=ocatid))

                    b = Cat.objects.get(pk=ocatid)
                    b.count = count
                    b.save()

                    return redirect('news_list')

                else:

                    fs = FileSystemStorage()
                    fs.delete(filename)

                    error = "Your File Is Bigger Than 5 MB"
                    return render(request, 'back/error.html' , {'error':error})

            else:

                fs = FileSystemStorage()
                fs.delete(filename)

                error = "Your File Not Supported"
                return render(request, 'back/error.html' , {'error':error})

        except:

            error = "Please Input Your Image"
            return render(request, 'back/error.html' , {'error':error})


    return render(request, 'back/news_add.html', {'cat':cat})
def news_delete(request,pk):
      # login check start
    if not request.user.is_authenticated :
        return redirect('mylogin')
    # login check end

    b=News.objects.get(pk=pk).writer
    if str(request.user) != str(b) :
        error = "Access Diend"
        return render(request, 'back/error.html' , {'error':error})

    try:

        b = News.objects.get(pk=pk)

        fs = FileSystemStorage()
        fs.delete(b.picname)

        b.delete()


    except:

        error = "Somthing Wrong"
        return render(request, 'back/error.html' , {'error':error})

    return redirect('news_list')
def news_edit(request,pk):
      # login check start
    if not request.user.is_authenticated :
        return redirect('mylogin')
    # login check end

    if len(News.objects.filter(pk=pk)) == 0 :
        error = "News Not Found"
        return render(request, 'back/error.html' , {'error':error})

    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0 :
        b=News.objects.get(pk=pk).writer
        if request.user != b :
            error = "Access Diend"
            return render(request, 'back/error.html' , {'error':error})



    news = News.objects.get(pk=pk)
    cat = SubCat.objects.all()

    if request.method == 'POST':

        newstitle = request.POST.get('newstitle')
        newscat = request.POST.get('newscat')
        newstxtshort = request.POST.get('newstxtshort')
        newstxt = request.POST.get('newstxt')
        catid = request.POST.get('newscat')
        tag=request.POST.get('tag')



        if newstitle == "" or newstxtshort == "" or newstxt == "" or newscat == "" :
            error = "All Fields Requirded"
            return render(request, 'back/error.html' , {'error':error})


        try :

            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            url = fs.url(filename)

            if str(myfile.content_type).startswith("image"):

                if myfile.size < 5000000 :

                    newsname = SubCat.objects.get(pk=catid).name

                    b = News.objects.get(pk=pk)

                    fss = FileSystemStorage()
                    fss.delete(b.picname)

                    b.name = newstitle
                    b.short_txt = newstxtshort
                    b.body_txt = newstxt
                    b.picname = filename
                    b.picurl = url
                    b.catname = newsname
                    b.catid = catid
                    b.tag=tag
                    b.act=0

                    b.save()

                    return redirect('news_list')

                else:

                    fs = FileSystemStorage()
                    fs.delete(filename)

                    error = "Your File Is Bigger Than 5 MB"
                    return render(request, 'back/error.html' , {'error':error})

            else:

                fs = FileSystemStorage()
                fs.delete(filename)

                error = "Your File Not Supported"
                return render(request, 'back/error.html' , {'error':error})

        except:

            newsname = SubCat.objects.get(pk=catid).name

            b = News.objects.get(pk=pk)

            b.name = newstitle
            b.short_txt = newstxtshort
            b.body_txt = newstxt
            b.catname = newsname
            b.catid = catid
            b.tag=tag
            b.tag=0

            b.save()

            return redirect('news_list')

    return render(request, 'back/news_edit.html', {'pk':pk, 'news':news, 'cat':cat})

def news_publish (request,pk):
    b=News.objects.get(pk=pk)
    b.act=1
    b.save()
    return redirect('news_list')

def news_unpublish (request,pk):
    b=News.objects.get(pk=pk)
    b.act=0
    b.save()
    return redirect('news_list')

def export_news_csv(request):
    responde=HttpResponse(content_type='text/csv')
    responde['Content_Disposition']='attachment;filename="newslist.csv"'
    writer=csv.writer(responde)
    writer.writerow(['title','writer'])
    for i in News.objects.all():
        writer.writerow([i.name,i.writer])
    return responde

def import_news_csv(request):
    if request.method=='POST':
        file=request.FILES['csv_file']
        if not file.name.endwith('csv'):
            error = "Please Input Csv File"
            return render(request, 'back/error.html' , {'error':error})
        if file.multiple_chunks():
            error = "File Too Large"
            return render(request, 'back/error.html' , {'error':error})
        file_data=file.read().decode('utf-8')
        lines=file_data.split('\n')
        for line in lines:
            field=line.split(',')
            try:
                if len(News.objects.filter(name=field[0])) and field[0] != 'title' and field[0] != "":
                    b=News(name=field[0])
                    b.save()
            except:
                print('finish')
    return redirect('news_list')

def news_all_show(request,word):
    site=Main.objects.get(pk=1)
    news=News.objects.filter(act=1).order_by('-pk')
    cat=Cat.objects.all()
    subcat=SubCat.objects.all()
    lastnews=News.objects.filter(act=1).order_by('-pk')[:3]
    popnews= News.objects.filter(act=1).order_by('-show')
    popnews2 = News.objects.filter(act=1).order_by('-show')[:3]
    trending=Trending.objects.all().order_by('-pk')[:5]
    lastnews2=News.objects.filter(act=1).order_by('-pk')[:4]
    cat1=Cat.objects.get(name=word).pk
    allnewss=News.objects.filter(catid=cat1)


    paginator=Paginator(allnewss,9)
    page=request.GET.get('page')
    try:
        allnews=paginator.page(page)
    except EmptyPage:
        allnews=paginator.page(paginator.num_page)
    except PageNotAnInteger:
        allnews=paginator.page(1)

    return render(request,'front/all_news.html',{'allnews':allnews,'lastnews2':lastnews2,'site':site,'news':news,'cat':cat,'subcat':subcat,'lastnews':lastnews,'popnews2':popnews2,'popnews':popnews,'trending':trending})

def allnews (request):
    site=Main.objects.get(pk=1)
    news=News.objects.filter(act=1).order_by('-pk')
    cat=Cat.objects.all()
    subcat=SubCat.objects.all()
    lastnews=News.objects.filter(act=1).order_by('-pk')[:3]
    popnews= News.objects.filter(act=1).order_by('-show')
    popnews2 = News.objects.filter(act=1).order_by('-show')[:3]
    trending=Trending.objects.all().order_by('-pk')[:5]
    lastnews2=News.objects.filter(act=1).order_by('-pk')[:4]
    allnewss=News.objects.all()


    paginator=Paginator(allnewss,9)
    page=request.GET.get('page')
    try:
        allnews=paginator.page(page)
    except EmptyPage:
        allnews=paginator.page(paginator.num_page)
    except PageNotAnInteger:
        allnews=paginator.page(1)

    return render(request,'front/allnews.html',{'allnews':allnews,'lastnews2':lastnews2,'site':site,
    'news':news,'cat':cat,'subcat':subcat,'lastnews':lastnews,'popnews2':popnews2,'popnews':popnews,'trending':trending})



def news_checkbox(request):
    if request.method=='POST':
        checks=request.POST.getlist('checks[]')
        for i in checks:
            b=News.objects.filter(pk=i)
            b.delete()
    return redirect('news_list')


# def News_Crawler():
#     list=Crawler()
#     for i in range(len(list)):
#         title=list[i]['title']
#         date=list[i]['date']
#         short_txt=list[i]['short_txt']
#         img=list[i]['img']
#         add=News.objects.create(name=title,short_txt=short_txt,body_txt=short_txt,date=date,picurl=img,writer='alireza')
#         add.save()
#