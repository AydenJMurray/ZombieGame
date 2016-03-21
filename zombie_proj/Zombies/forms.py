from django import forms
from django.contrib.auth.models import User
from Zombies.models import Player

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        #fields = ('profile_picture',)
