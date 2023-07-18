from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Classes
class RegistrationForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    email = forms.EmailField(label="Email", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput,label="Password", max_length=100)

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(widget=forms.PasswordInput,label="Password", max_length=100)
    
class ChangePasswordForm(forms.Form):
    currpassword = forms.CharField(widget=forms.PasswordInput,label="Current Password", max_length=100)
    newpassword = forms.CharField(widget=forms.PasswordInput,label="New Password", max_length=100)
    cnfpassword = forms.CharField(widget=forms.PasswordInput,label="Confirm Password", max_length=100)


# Create your views here.
def loginpage(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Change the render to dashboard 
                return redirect('index')
            else:
                messages.info(request, "Invalid Login Credentials")  
    else:   
        form = LoginForm()    

    return render(request, "authentication/login.html", {
        "form" : LoginForm()
    })
    
def registerpage(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            
            user = User.objects.filter(username = username)
            if user.exists():
                messages.info(request, "Username already in use")  
                return render(request, "authentication/register.html", {
                    "form" : form
                })
            
            user = User.objects.create_user(
                username = username,
                email = email
            )     
            user.set_password(password)
            user.save()  
            # Change the render to dashboard 
            return redirect('index')
    else:   
        form = RegistrationForm()
    
    return render(request, "authentication/register.html", {
        "form" : RegistrationForm()
    })

@login_required(login_url="loginpage")
def logoutbtn(request):
    logout(request)
    return redirect('loginpage')

@login_required(login_url="loginpage")
def changepassword(request):
    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            currpassword = form.cleaned_data["currpassword"]
            newpassword = form.cleaned_data["newpassword"]
            cnfpassword = form.cleaned_data["cnfpassword"]
            username = request.user.username

            user = authenticate(request, username=username, password=currpassword)
            if cnfpassword==newpassword:
                if user is not None: 
                    if(newpassword!=currpassword):
                        u = User.objects.get(username=username)
                        u.set_password(newpassword)
                        u.save()
                        messages.info(request, "Password has been Updated")
                    else:
                        messages.info(request, "New Password and Current Password cannot be same")
                else:
                    messages.info(request, "Please enter the correct password")
            else:
                messages.info(request, "The New and Confirm Password do not match")
    else:   
        form = ChangePasswordForm()
    
    return render(request, "authentication/changePassword.html", {
        "form" : form,
        "username" : request.user.username
    })
