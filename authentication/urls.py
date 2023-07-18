from django.urls import path
from . import views

urlpatterns = [
    path('login',views.loginpage,name='loginpage'),
    path('register',views.registerpage,name='registerpage'),
    path('logout',views.logoutbtn,name='logout'),
    path('changepassword',views.changepassword,name='changepassword'),
]
