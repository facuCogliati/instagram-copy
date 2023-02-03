from django.contrib import admin
from .models import Post, SavePost, Comment, Histories, Notifications, Likes
# Register your models here.

admin.site.register(Post)
admin.site.register(SavePost)
admin.site.register(Comment)
admin.site.register(Histories)
admin.site.register(Notifications)
admin.site.register(Likes)

