from django.shortcuts import render,redirect
from .models import Token
from news.models import News
from subcat.models import SubCat
from trending.models import Trending
from cat.models import Cat
from manager.models import Manager
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User,Permission,Group
import random
from django.conf import settings
from django.core.mail import send_mail



def token (request):

    if request.method=='POST':
        email=request.POST.get('email')
        if email=='':
            msg = "pls input your email"
            return render(request, 'front/msgbox.html', {'msg':msg})
        if not len(User.objects.filter(email=email)) == 0:
            msg = "this email is already exist"
            return render(request, 'front/msgbox.html', {'msg':msg})
        a=Token.objects.filter(email=email)
        a.delete()
        rand=""
        for i in range(4):
            rand=rand+str(random.randint(0,9))
        #send securty code to email
        r=Token(token=rand,email=email)
        r.save()
        pk=Token.objects.get(token=rand).pk

        txt='hello     wellcome to magenews           your security code for register is : '+str(rand)
        email_to=email
        subject='magenews'
        message=txt
        email_from=settings.EMAIL_HOST_USER
        emails=[email_to]
        send_mail(subject,message,email_from,emails)


        #c=Token.objects.filter(email=word)


    return redirect('myregister',email,pk)
