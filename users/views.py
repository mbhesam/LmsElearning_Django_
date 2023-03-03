from django.shortcuts import render
from .forms import ProfileUser
from  django.http import HttpResponse ,HttpResponseRedirect
from .authentication import EmailAuthBackend
from django.contrib.auth import login , logout
from django.urls import reverse
from django.core.exceptions import ValidationError

def index(request):
    return HttpResponse("this is home page")

def register(request):
    registered = False
    if request.method=='POST':
        pu = ProfileUser(data=request.POST)
        if pu.is_valid():
            pu.save().save()
            registered=True
        else:
            pass
    else:
        pu = ProfileUser(data=request.GET)
    return render(request, 'users/registration.html',
                          {
                              'registered': registered,
                              'ProfileUser': pu
                          })

def userlogin(request):
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = EmailAuthBackend.authenticate(email=email,password=password)
        if user != None:
            login(request,user)
            return  HttpResponseRedirect(reverse('index'))
        else:
            return HttpResponse('Your Email or Password is incorrect')
    else:
        return render(request,'users/login.html')

def userlogout(request):
    if request.user.is_authenticated:
       logout(request)
       return HttpResponseRedirect(reverse('base.html'))


