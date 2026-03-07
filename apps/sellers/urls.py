from django.urls import path
from apps.sellers.views import seller_login
from apps.sellers.views import seller_onboarding , seller_register
urlpatterns = [
   
    path("login/", seller_login, name="seller_login"),
    path("register/", seller_register, name="seller_register"),
    path("info/", seller_onboarding),  
]



