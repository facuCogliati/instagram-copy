from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(default='avatar.svg')
    follow = models.ManyToManyField(User, blank=True, related_name= 'follow')
    followers = models.ManyToManyField(User, blank=True, related_name= 'followers')

    def __str__(self):
        return self.name