from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages
from .models import Rooms, Topic, Message
from django.db.models import Q 
from .forms import UserRoom
# Create your views here.



# rooms = [
#     {'id': 1, 'name': 'Lets start learning python'},
#     {'id': 2, 'name': 'Learn with me'},
#     {'id': 3, 'name': 'Learning javascript'},
#     {'id': 4, 'name': 'Fun with code'},
# ]

def loginPage(request):
    page = 'login'
    if request.method == 'POST':
        # get username and password form user input 
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        # check this user exit or not 
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exit')

        # if user exit make sure the credential is correct or not 
        user = authenticate(request,username=username, password=password)
        
        # login user and create the session on db browser and redirect home page 
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exit')
      
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutPage(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registrations')

    context = {'form':form}
    return render(request, 'base/login_register.html',context)

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
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))

    context = {'rooms': rooms,'topics':topics, 'room_count': room_count, 'room_messages':room_messages}
    return  render(request, 'base/home.html',context)

def room(request,pk):
    room = Rooms.objects.get(id=pk)

    room_messages = room.message_set.all().order_by('-created')  #sob ses e eita abr dekhte hobe
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)  
        # for post request to match some functionality and fully reload this page and back to the same page as well
        

    context = { 'room': room, 'room_messages': room_messages, 'participants':participants}
    return render(request, 'base/room.html',context)

@login_required(login_url='login')
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

@login_required(login_url='login')
def update_room(request,pk):
    room = Rooms.objects.get(id=pk)
    form = UserRoom(instance=room)

    if request.user != room.host:
        return HttpResponse('You are no allowed here.')

    if request.method == 'POST':
        form = UserRoom(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def delete_room(request,pk):
    room = Rooms.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are no allowed here.')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'obj':room}
    return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def delete_message(request,pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are no allowed here.')

    if request.method == 'POST':
        message.delete()
        # return redirect('room', pk=message.room.id)
        return redirect('home')
    context = {'obj':message}
    return render(request, 'base/delete.html', context)