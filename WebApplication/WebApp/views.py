from django.shortcuts import  redirect, render, get_object_or_404
from django.contrib.auth.hashers import check_password
from django.views.decorators.cache import cache_control
from .forms import UserForm, EditUserForm
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

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
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



def logout(request):
    request.session.flush()  
    return redirect('login')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = UserInfo.objects.get(pk=user_id)
        username = user.username
    else:
        username = 'Guest'
    return render(request, 'home.html', {'username': username})


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