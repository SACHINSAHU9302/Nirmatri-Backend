from django.urls import path
from .views import user_login, get_profile, update_profile

urlpatterns = [
   
    path("login/", user_login),
    path("profile/", get_profile),
    path("profile/update/", update_profile),
]
