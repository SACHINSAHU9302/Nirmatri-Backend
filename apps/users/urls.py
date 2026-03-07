from django.urls import path
from .views import user_login, get_profile, update_profile, logout_user

urlpatterns = [
    path("login/", user_login),
    path("logOut/", logout_user),
    path("userinfo/", get_profile),
    path("profile/update/", update_profile),
]
