from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from . models import User
from . forms import RegisterUserForm, UpdateUserForm

# Create your views here.

@login_required
def update_profile(request):
    user = request.user
    form = UpdateUserForm(instance=user)

    if request.method == 'POST':
        form = UpdateUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile update!')
            return redirect('my_profile')
        else:
            messages.success(request, 'Ups... Something went wrong')
            
    return render(request, 'users/update_profile.html', {'form':form})



@login_required
def profiles(request, pk):
    user =  User.objects.get(pk=pk)
    rooms = user.room_set.all()
    return render(request, "users/profiles.html", {'user':user, 'rooms':rooms})

@login_required
def my_profile(request):
     user = request.user
     rooms = user.room_set.all()
     return render(request, 'users/my_profile.html', {'rooms':rooms})


def register_page(request):
    form = RegisterUserForm()

    if request.method == 'POST':
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.emai = user.email.lower()
            user.save()
            login(request, user)
            messages.success(request, 'Account created!')
            return redirect('home')
        else:
            messages.success(request, 'An error ocurred during registration')
    return render(request, 'users/register.html', {'form': form})

#logout function
def logout_user(request):
    logout(request)
    messages.success(request, 'See you later')
    return redirect('login_page')


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.success(request, "User does not exists! ")
        
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request,  "Welcome back " + user.email)
            return redirect('home')
        else:
            messages.success(request, 'Username or password not match!')

    return render(request, 'users/login.html')