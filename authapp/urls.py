from django.urls import path
from .views import (
    home,
    register,
    login,
    seller_register,
    forgot_password,
    reset_password,
)

urlpatterns = [
    # ================= USER AUTH =================
    path("login/", login, name="login"),
    path("userRegister/", register, name="user_register"),

    # ================= SELLER AUTH =================
    path("sellerRegister/", seller_register, name="seller_register"),

    # ================= PASSWORD RESET =================
    path("forgot-password/", forgot_password, name="forgot_password"),
    path("reset-password/", reset_password, name="reset_password"),
]
