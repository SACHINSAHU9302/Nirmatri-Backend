from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("api/auth/", include("apps.users.urls")),   # ← IMPORTANT
    path("api/seller/", include("apps.sellers.urls")),
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("api/admin/", include("apps.superadmin.urls")),
]