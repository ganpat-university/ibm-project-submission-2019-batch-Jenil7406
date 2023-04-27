from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def home(request):
    return(render(request,"index.html"))

def login_user(request):
    if request.method=='POST':  
        account = request.POST['account_input']

        if User.objects.filter(username=account):
            user = authenticate(username=account, password=account)
            login(request,user)
            messages.success(request,"Logged In Successfully")
            return redirect('home')

        newuser = User.objects.create_user(account,account,account)
        newuser.save()
        messages.success(request,"Account Created and Logged In Successfully")
        return redirect('home')
    
    return(render(request,"login.html"))

def logout_user(request):
    logout(request)
    messages.success(request,"Loggged Out Successfully")
    return redirect('home')
