from django.urls import path
from apps.users.views import (
    user_login,
    user_register,
    forgot_password,
    reset_password,
)
urlpatterns = [
    # ================= USER AUTH =================
    path("login/", user_login, name="login"),
    path("userRegister/", user_register, name="user_register"),

    # ================= PASSWORD RESET =================
    path("forgot-password/", forgot_password, name="forgot_password"),
    path("reset-password/", reset_password, name="reset_password"),
]
