from django.urls import path ,include
from .views import index,register,userlogin,userlogout
urlpatterns = [
    path('',index,name='index'),
    path('register',register,name='register'),
    path('login',userlogin,name='login'),
    path('logout',userlogout,name='logout')
]