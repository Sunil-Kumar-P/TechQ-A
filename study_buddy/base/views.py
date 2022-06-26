from pickle import GET
from django.shortcuts import render, redirect
from .models import Room, Topic
from .forms import RoomForm



#home page
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(topic__name__icontains=q)
    topics = Topic.objects.all()
    context =  {'rooms':rooms, 'topics':topics}
    return render(request,'base/home.html',context)

#room page
def room(request,pk):
    room = Room.objects.get(id=pk)
    context =  {'room':room}
    return render(request,'base/room.html',context)


def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'base/room_form.html', context)