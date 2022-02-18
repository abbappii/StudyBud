from django.shortcuts import render

from .models import Rooms
from .forms import UserRoom
# Create your views here.



# rooms = [
#     {'id': 1, 'name': 'Lets start learning python'},
#     {'id': 2, 'name': 'Learn with me'},
#     {'id': 3, 'name': 'Learning javascript'},
#     {'id': 4, 'name': 'Fun with code'},
# ]


def home(request):
    rooms = Rooms.objects.all()
    context = {'rooms': rooms}
    return  render(request, 'base/home.html',context)

def room(request,pk):
    room = Rooms.objects.get(id=pk)
    context = { 'room': room}
    return render(request, 'base/room.html',context)

def create_room(request):
    form = UserRoom()
    context = {'form': form}
    return render(request, 'base/room_form.html', context)

