from django.shortcuts import render
from .forms import ProfileUser
from  django.http import HttpResponse ,HttpResponseRedirect
from .authentication import EmailBackend
from django.contrib.auth import login , logout
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ValidationError

def index(request):
    return render(request,'base.html',{"user":request.user})

def register(request):
    registered = False
    if request.method=='POST':
        pu = ProfileUser(request.POST,request.FILES)
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
        user = EmailBackend.authenticate(request=request,username=email,password=password)
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
        return HttpResponseRedirect(reverse_lazy('index'))
    else:
        return HttpResponse('you are not login')

