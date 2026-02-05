from django.urls import path
from .views import home, register, login

urlpatterns = [
    path("userRegister/", register, name="user_register"),
    path("sellerRegister/", login, name="seller_register"),
]
