from django.forms import forms
from django.forms import ModelForm
from .models import Rooms

class UserRoom(ModelForm):
    class Meta:
        model = Rooms
        fields = '__all__'
