from django.shortcuts import redirect, render
from .models import Rooms, Topic
from django.db.models import Q 
from .forms import UserRoom
# Create your views here.



# rooms = [
#     {'id': 1, 'name': 'Lets start learning python'},
#     {'id': 2, 'name': 'Learn with me'},
#     {'id': 3, 'name': 'Learning javascript'},
#     {'id': 4, 'name': 'Fun with code'},
# ]


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else '' 
    # 'q' defer what we pass on url  
    print(q)  
    rooms = Rooms.objects.filter(Q(topic__name__icontains =q) |
        Q(description__icontains=q) | 
        Q(name__icontains=q)
        )
    
    topics = Topic.objects.all()
    room_count = rooms.count()

    context = {'rooms': rooms,'topics':topics, 'room_count': room_count}
    return  render(request, 'base/home.html',context)

def room(request,pk):
    room = Rooms.objects.get(id=pk)
    context = { 'room': room}
    return render(request, 'base/room.html',context)

def create_room(request):
    form = UserRoom() #form
    if request.method == 'POST': #post data
        # user data add korlei form e vlaue pathai deoyar 
        # jonno UserForm e request.POST pathai deoya 
        form = UserRoom(request.POST) #form e post data pathai deoya
        if form.is_valid(): #value valid kina 
            form.save() #valid hoile save kora
            return redirect('home')  #save hoile home page e niye jaoya
    context = {'form': form,}  #form ke context hisebe html e file e pathano
    return render(request, 'base/room_form.html', context)  # render kora html form e jekhane value niye kaj kora jabe

def update_room(request,pk):
    room = Rooms.objects.get(id=pk)
    form = UserRoom(instance=room)
    if request.method == 'POST':
        form = UserRoom(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'base/room_form.html', context)


def delete_room(request,pk):
    room = Rooms.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj':room}
    return render(request, 'base/delete.html', context)