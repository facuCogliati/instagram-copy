from django.urls import path
from . import views

urlpatterns = [
    path('messanger-inbox', views.messanger, name="messages"),
    path('messanger/<str:pk>', views.displayMessanger, name="messages-display"),
    path('ajax-display', views.ajaxDisplay, name="message-ajax-display"),
    path('send-post/<str:pk>', views.send_post, name="send-post"),

    path('received-newMessage', views.newMessagesReceived, name='received-messages'),
]