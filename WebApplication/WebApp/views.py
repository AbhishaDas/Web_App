#view.py
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from . forms import UserForm
from WebApp.models import userinfo

# Create your views here.
def signup(request):
    if request.POST:
        frm=UserForm(request.POST)
        if frm.is_valid():
            frm.save()
            return redirect('login')
    else:
        frm=UserForm()
        
    return render(request,'signup.html',{'frm':frm})

def login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        
        print("Username:", username)
        print("Password:", password)
        
        user= authenticate(request,username=username,password=password)
        if user is not None:
            
            print("User authenticated successfully.")
            
            auth_login(request, user)
            return redirect('home')
        else:
            
            print("Authentication failed.")
            
            return render(request, 'login.html', {'error':'Invalid Username or Password'})
    return render(request, 'login.html')   


def home(request):
    return render(request, 'home.html') 