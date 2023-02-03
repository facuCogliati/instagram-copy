from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('session-login', views.session_login, name="login"),
    path('session-logout', views.session_logOut, name="logout"),
    path('session-register', views.session_register, name="register"),

    path('<str:pk>', views.profile_page, name="profile"),
    path('edit-profile/<str:pk>', views.edit_profile, name="edit_profile"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)