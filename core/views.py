from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Room, Like
from . forms import RoomForm
from users.models import User

# Create your views here.

def search(request):
    query = request.GET.get('query', '')
    rooms = Room.objects.filter(name__icontains=query)
    return render(request, 'core/search.html', {'query':query, 'rooms':rooms})

def delete_room(request, pk):
    room = Room.objects.get(pk=pk)
    if request.user == room.user:
        room.delete()
        messages.success(request, 'Room Delete')
        return redirect('my_profile')
    else:
        messages.success(request, 'Ups... you dont own this room')
        return redirect('home')


def update_room(request, pk):
    room = Room.objects.get(pk=pk)
    form = RoomForm(request.POST or None, instance= room)
    if request.user == room.user:
        if form.is_valid():
            form.save()
            messages.success(request, 'Room Update')
            return redirect('my_profile')
    else:
            messages.success(request, 'Ups... you dont own this room')
            return redirect('home')
    return render(request, 'core/update_room.html', {'form':form})

def create_room(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.user = request.user
            room.save()
            messages.success(request, 'Room created!')
            return redirect('home')
        else:
            messages.success(request, 'Ups there was a problem created!')

    return render(request, 'core/create_room.html', {'form': form})
        


def room(request):
    return render(request, 'core/room.html')


def home(request):
    user = request.user
    users = User.objects.exclude(username=user.username)
    filtro = users[0:5]

    rooms = Room.objects.all()

    paginator = Paginator(rooms, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'core/home.html', {'page_obj':page_obj, 'filtro':filtro})

