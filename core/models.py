from django.db import models
from django.contrib.auth.models import User
from usuarios.models import Profile
# # Create your models here.

class Post(models.Model):
    host = models.ForeignKey(Profile, on_delete=models.CASCADE)
    imagen = models.ImageField(null=False)
    description = models.TextField(max_length=180, blank=True)
    like = models.PositiveIntegerField(default=0)
    tagged = models.ManyToManyField(User, blank=True, related_name='tagged')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description

class Comment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    postcomments = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='postcomments')
    name = models.CharField(max_length=130, blank=True)
    def __str__(self):
        return self.name

class SavePost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.post)

class Histories(models.Model):
    # acodarte de renombrarlo
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='histories')
    history = models.ImageField(blank=False)
    description = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    permanent = models.BooleanField(default=False)
    expired = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.description)
        
class Notifications(models.Model):
    type = models.IntegerField(default=1)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_noti')
    see = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.type)

class Likes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post+')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user+')

    def __str__(self):
        return str(self.post)
