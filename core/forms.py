from django import forms
from .models import Post, Histories

class PostCreation(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'tagged', 'imagen']


class HistoryCreation(forms.ModelForm):
    class Meta:
        model = Histories
        fields = ['history', 'description', 'permanent']