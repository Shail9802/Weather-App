from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
# Create your views here.

def signup(request):
    if request.method=='GET':
        return render(request,"signupacc.html",{"form":UserCreationForm})
    else:
        if request.POST['password1']==request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST["username"],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('Home')
            except IntegrityError:
                return render (request,'signupacc.html',{"form":UserCreationForm,'error':'Username already taken'})
        else:
            return render(request,"signupacc.html",{"form":UserCreationForm,"error":"Password does not match"})
        
def logoutAccount(request):
    logout(request)
    return redirect('Home')

def loginAccount(request):
    if request.method=="GET":
        context = {"form":AuthenticationForm}
        # return render(request,'loginAcc.html')
        return render(request,"login.html",context)
    else:
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])

        if user is None:
            context = {"form":AuthenticationForm,"error":"Password does not match"}
            # return render(request,'loginAcc.html',context)
            return render(request,"login.html",context)
        
        else :
            login(request,user)
            return redirect('Home')