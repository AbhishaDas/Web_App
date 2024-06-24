from django.shortcuts import redirect, render
from django.contrib.auth.hashers import check_password
from .forms import UserForm
from .models import UserInfo

def signup(request):
    if request.POST:
        frm = UserForm(request.POST)
        if frm.is_valid():
            frm.save()
            return redirect('login')
    else:
        frm = UserForm()
        
    return render(request, 'signup.html', {'frm': frm})

def login_user(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        
        print("Username:", username)
        print("Password:", password)
        
        try:
            user = UserInfo.objects.get(username=username)
            if check_password(password, user.password):
                print("User authenticated successfully.")
             
                request.session['user_id'] = user.pk
                return redirect('home')
            else:
                print("Authentication failed.")
                return render(request, 'login.html', {'error': 'Invalid Username or Password'})
        except UserInfo.DoesNotExist:
            print("Authentication failed.")
            return render(request, 'login.html', {'error': 'Invalid Username or Password'})
    
    return render(request, 'login.html')   

from django.shortcuts import redirect

def logout(request):
    request.session.flush()  
    return redirect('login')

def home(request):
    return render(request, 'home.html')

username = 'admin'
password = 'admin123'


def admin_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username == username and password == password:
            return redirect('admin_home')
        else:
            return render(request, 'admin_login.html', {'error': 'Invalid username or password'})

    return render(request, 'admin_login.html')

def admin_home(request):
     user_details = UserInfo.objects.all()
     print(user_details)
     return render(request,'admin_home.html',{'users' :user_details})