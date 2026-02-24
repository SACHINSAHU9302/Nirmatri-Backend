from django.urls import path
from .views import superadmin_login, get_pending_sellers, approve_seller

urlpatterns = [
    path("login/", superadmin_login),
    path("pending-sellers/", get_pending_sellers),
    path("approve/<str:seller_id>/", approve_seller),
]