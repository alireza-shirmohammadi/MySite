from django.shortcuts import render,redirect
from .models import Manager
from news.models import News
from subcat.models import SubCat
from trending.models import Trending
from cat.models import Cat
from manager.models import Manager
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User, Group

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

def manager_group (request):
     # login check start
    if not request.user.is_authenticated :
        return redirect('mylogin')
    # login check end


    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0 :
        error = "Access Denied"
        return render(request, 'back/error.html' , {'error':error})


    group=Group.objects.all()

    return render (request,'back/manager_group.html',{'group':group})

def manager_group_add (request):
     # login check start
    if not request.user.is_authenticated :
        return redirect('mylogin')
    # login check end


    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0 :
        error = "Access Denied"
        return render(request, 'back/error.html' , {'error':error})

    if request.method == 'POST':
        name = request.POST.get('name')
        if not name == "":
            if len (Group.objects.filter(name=name))==0 :
                group=Group(name=name)
                group.save()
            else:
                error = "This Group Name Is Already Exist."
                return render(request, 'back/error.html' , {'error':error})
    return redirect('manager_group')

def manager_group_del (request,name):
     # login check start
    if not request.user.is_authenticated :
        return redirect('mylogin')
    # login check end


    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0 :
        error = "Access Denied"
        return render(request, 'back/error.html' , {'error':error})

    group = Group.objects.filter(name=name)
    group.delete()
    return redirect('manager_group')

def users_groups(request,pk):
     # login check start
    if not request.user.is_authenticated :
        return redirect('mylogin')
    # login check end


    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0 :
        error = "Access Denied"
        return render(request, 'back/error.html' , {'error':error})

    manager=Manager.objects.get(pk=pk)
    user=User.objects.get(username=manager.utext)
    ugroup=[]
    for i in user.groups.all():
        ugroup.append(i.name)

    group=Group.objects.all()

    return render(request,'back/users_groups.html',{'group':group,'ugroup':ugroup,'pk':pk})

def add_users_to_groups(request,pk):
     # login check start
    if not request.user.is_authenticated :
        return redirect('mylogin')
    # login check end


    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0 :
        error = "Access Denied"
        return render(request, 'back/error.html' , {'error':error})

    if request.method == 'POST':
        gname=request.POST.get('gname')
        group=Group.objects.get(name=gname)
        manager=Manager.objects.get(pk=pk)
        user=User.objects.get(username=manager.utext)
        user.groups.add(group)

    return redirect('users_groups' , pk=pk)

def del_users_to_groups(request,pk,name):
     # login check start
    if not request.user.is_authenticated :
        return redirect('mylogin')
    # login check end


    perm = 0
    for i in request.user.groups.all():
        if i.name == "masteruser" : perm = 1

    if perm == 0 :
        error = "Access Denied"
        return render(request, 'back/error.html' , {'error':error})

    manager=Manager.objects.get(pk=pk)
    group=Group.objects.get(name=name)
    user=User.objects.get(username=manager.utext)
    user.groups.remove(group)
    return redirect('users_groups', pk=pk)
