from django.urls import path
from .views import google_login
from .views import user_login, get_profile, update_profile

urlpatterns = [
    path("google-login/", google_login),
    path("login/", user_login),
    path("profile/", get_profile),
    path("profile/update/", update_profile),
]
