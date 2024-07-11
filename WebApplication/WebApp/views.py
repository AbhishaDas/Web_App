from django.shortcuts import  redirect, render, get_object_or_404
from django.contrib.auth.hashers import check_password
from .forms import UserForm, EditUserForm
from .models import UserInfo
from django.contrib.auth.decorators import login_required
from . middleware import NoCacheMiddleware
from django.utils.decorators import decorator_from_middleware


cache_control_no_cache = decorator_from_middleware(NoCacheMiddleware)

def signup(request):
    if request.POST:
        frm = UserForm(request.POST)
        if frm.is_valid():
            frm.save()
            return redirect('login')
    else:
        frm = UserForm()
        
    return render(request, 'signup.html', {'frm': frm})

@cache_control_no_cache
def login_user(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        
        print("Username:", username)
        print("Password:", password)
        
        try:
            user = UserInfo.objects.get(username=username)
            if check_password(password, user.password):
             
                request.session['user_id'] = user.pk
                return redirect('home')
            
            else:
                error_message = 'Invalid Username or Password'
            
        except UserInfo.DoesNotExist:
                error_message = 'Invalid Username or Password'
                
        return render(request, 'login.html',  {'error': error_message})
    
    return render(request, 'login.html')   



def logout(request):
    request.session.flush()  
    return redirect('login')

@cache_control_no_cache
def home(request):
    user_id = request.session.get('user_id')
    if user_id:
        try:
            user = UserInfo.objects.get(pk=user_id)
            username = user.username
        except UserInfo.DoesNotExist:
            # Handle the case where the user_id is in the session but the user no longer exists
            request.session.flush()
            username = 'Guest'
        
    else:
        username = 'Guest'
    return render(request, 'home.html', {'username': username})


admin_username = 'admin'
admin_password = 'admin123'


def admin_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username == admin_username and password == admin_password:
            return redirect('admin_home')
        else:
            return render(request, 'admin_login.html', {'error': 'Invalid username or password'})

    return render(request, 'admin_login.html')


@cache_control_no_cache
def admin_home(request):
    query = request.GET.get('q')
    if query:
        user_details = UserInfo.objects.filter(
            firstname__icontains=query) | UserInfo.objects.filter(
            lastname__icontains=query) | UserInfo.objects.filter(
            email__icontains=query) | UserInfo.objects.filter(
            username__icontains=query)
    else:
        user_details = UserInfo.objects.all()
        
    return render(request, 'admin_home.html', {'users': user_details})

 

def manage_user(request, user_id):
    user = get_object_or_404(UserInfo, pk=user_id)
    if request.POST:
        if 'save' in request.POST:
            frm = EditUserForm(request.POST, instance=user)
            if frm.is_valid():
                frm.save()
                return redirect('admin_home')
        elif 'delete' in request.POST:
            user.delete()
            return redirect('admin_home')
    else:
        frm = EditUserForm(instance=user)
    
    return render(request, 'manage_user.html', {'frm': frm, 'user': user})