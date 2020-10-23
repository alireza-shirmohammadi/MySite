from django.shortcuts import render,redirect
from .models import Manager
from news.models import News
from subcat.models import SubCat
from trending.models import Trending
from cat.models import Cat
from manager.models import Manager
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User, Group , Permission
from django.contrib.contenttypes.models import ContentType

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

def manager_perms (request):
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
    perms= Permission.objects.all()
    return render(request,'back/manager_perms.html',{'perms':perms})

def manager_perms_del (request,name):
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

    perm=Permission.objects.filter(name=name)
    perm.delete()

    return redirect('manager_perms')
def manager_perms_add(request):
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

    if request.method=='POST':
        name=request.POST.get('name')
        cname=request.POST.get('cname')
        contenttype=ContentType.objects.get(app_label='main',model='main')
        if len(Permission.objects.filter(codename=cname))==0:
            perm=Permission(name=name,codename=cname,content_type=contenttype)
            #permission = Permission.objects.create(codename=cname, name=name, content_type=content_type)
            perm.save()
        else:
            error = "This Codename Used Before"
            return render(request, 'back/error.html' , {'error':error})

        return redirect('manager_perms')

def users_perms (request,pk):
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
    permission=Permission.objects.filter(user=user)
    uperms=[]
    for i in permission:
        uperms.append(i.name)
    perms = Permission.objects.all()
    return render(request,'back/users_perms.html',{'uperms':uperms,'perms':perms,'pk':pk})

def users_perms_del (request,pk,name):
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
    permission=Permission.objects.get(name=name)
    user.user_permissions.remove(permission)
    return redirect('users_perms',pk=pk)

def users_perms_add (request,pk):
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

    if request.method=='POST':
        pname=request.POST.get('pname')

        manager=Manager.objects.get(pk=pk)
        user=User.objects.get(username=manager.utext)
        permission=Permission.objects.get(name=pname)
        user.user_permissions.add(permission)
    return redirect('users_perms',pk=pk)

def groups_perms (request,name):
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

    group=Group.objects.get(name=name)
    perms=group.permissions.all()
    allperms=Permission.objects.all()
    return render(request,'back/groups_perms.html',{'perms':perms,'allperms':allperms,'name':name})

def groups_perms_del(request,gname,name):
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

    group=Group.objects.get(name=gname)
    perm=Permission.objects.get(name=name)
    group.permissions.remove(perm)

    return redirect('groups_perms',name=gname)

def groups_perms_add(request,name):
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
        
    if request.method=='POST':
        pname=request.POST.get('pname')
        group=Group.objects.get(name=name)
        perm=Permission.objects.get(name=pname)
        group.permissions.add(perm)

    return redirect('groups_perms',name=name)
