from django.shortcuts import render,redirect
from .models import Manager
from news.models import News
from subcat.models import SubCat
from trending.models import Trending
from cat.models import Cat
from manager.models import Manager
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User

def manager_list (request):
     # login check start
        if not request.user.is_authenticated :
            return redirect('mylogin')
        # login check end
        manager = Manager.objects.all()


        return render(request,'back/manager_list.html',{'manager':manager})

def manager_del (request,pk):
     # login check start
        if not request.user.is_authenticated :
            return redirect('mylogin')
        # login check end

        manager = Manager.objects.get(pk=pk)
        user = User.objects.filter(username=manager.utext)
        user.delete()
        manager.delete()

        return redirect('manager_list')
