from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm

from WebApplication.WebApp.forms import UserForm

# Create your views here.
def signup(request):
    if request.POST:
        frm=UserForm(request.POST)
        if frm.is_valid():
            frm.save()
            return redirect('login')
    else:
        frm=UserForm()
        
    return render(request,'signup.html',{frm:'frm'})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Assuming 'home' is the name of the URL pattern for the home view
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')
    