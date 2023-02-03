from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms.widgets import TextInput, PasswordInput
from .models  import Profile


class profileForm(UserCreationForm):
    class Meta: 
        model = User
        fields = ['username', 'first_name', 'email', 'password1', 'password2',]
        # widgets = {
        #     'username': TextInput(attrs={'placeholder': 'Username'}),
        #     'email': TextInput(attrs={'placeholder': 'Email'}),
        #     'password': PasswordInput(attrs={'placeholder': 'Password'}),
        #     'password2': PasswordInput(attrs={'placeholder': 'Confirm Password'})
        # }

        

class UserProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'name', 'bio', ]