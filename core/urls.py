from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),

    path('save-post', views.save_post, name="savepost"),
    path('like-post', views.like_post, name="likepost"),
    path('create-post', views.createPost, name='createPost'),

    path('create-history', views.CreateHistory, name='createHistory'),
    path('historyJson', views.historyJson, name='historyJson'),

    path('notifications/<str:pk>', views.notifications_user, name='notifications'),

    path('post/<str:pk>', views.postUser, name='postUser'),
    path('create-Comment', views.createComment, name='createComment'),
    path('delete-Comment', views.deleteComment, name='deleteComment'),

      
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)