from django.db import models
from django.contrib.auth.models import User
from usuarios.models import Profile
from core.models import Post

# Create your models here.
class Message(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sende_user')
    received = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receive_user')
    postsended = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)
    body = models.CharField(max_length=200, blank = True)
    created = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return str(self.body) or str(self.postsended)