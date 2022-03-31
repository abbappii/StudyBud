from pyexpat import model
from django.forms import forms
from django.forms import ModelForm
from .models import Rooms, User


class UserRoom(ModelForm):
    class Meta:
        model = Rooms
        fields = '__all__'
        exclude = {'host','participants'}

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
