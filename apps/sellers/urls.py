from django.urls import path
from .views import seller_login, seller_register
from .views import seller_onboarding
urlpatterns = [
   
    path("login/", seller_login, name="seller_login"),
    path("register/", seller_register, name="seller_register"),
    path("register/", seller_register),
    path("info/", seller_onboarding),  
]



