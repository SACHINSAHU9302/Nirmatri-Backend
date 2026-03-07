from django.urls import path
from apps.users.views import (
    user_login,
    user_register,
    get_profile,
    update_profile,
    reset_password,
    forgot_password,
)
urlpatterns = [
    # ================= USER AUTH =================
    path("login/", user_login, name="login"),
    path("userRegister/", user_register, name="user_register"),
    path("profile/",get_profile, name="get_profile"),
    path("profile/update/",update_profile, name="update_profile"),

    
    # ================= PASSWORD RESET =================
    path("forgot-password/", forgot_password, name="forgot_password"),
    path("reset-password/", reset_password, name="reset_password"),
]
