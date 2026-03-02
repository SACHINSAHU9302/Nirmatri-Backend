from django.urls import path
from .views import google_login, get_profile, google_logout

urlpatterns = [
    path("google-login/", google_login),
    path("logout/", google_logout),
    path("profile/", get_profile),
]