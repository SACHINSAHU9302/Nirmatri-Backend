from apps.users.googleauth.services import verify_google_token, get_or_create_google_user
from rest_framework.response import Response
from rest_framework.decorators import api_view
from apps.users.models import GoogleUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.conf import settings
from datetime import datetime, timedelta
import jwt




@api_view(["POST"])
def google_login(request):
    token = request.data.get("token")

    idinfo = verify_google_token(token)

    if not idinfo:
        return Response({"error": "Invalid token"}, status=400)

    user, created = get_or_create_google_user(idinfo)

    # 🔐 CREATE JWT
    payload = {
        "user_id": str(user.id),
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(days=7),
        "iat": datetime.utcnow(),
    }

    jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    return Response({
        "token": jwt_token,
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "picture": user.picture
        }
    })

@api_view(["POST"])
def google_logout(request):
    try:
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"error": "Refresh token required"}, status=400)

        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({"message": "Logout successful"})

    except Exception:
        return Response(
            {"error": "Invalid token"},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(["GET"])
def get_profile(request):
    email = request.query_params.get("email")

    if not email:
        return Response({"error": "Email is required"}, status=400)

    try:
        user = GoogleUser.objects.get(email=email)
    except GoogleUser.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    return Response({
        "email": user.email,
        "name": user.name,
        "picture": user.picture,
        "auth_provider": user.auth_provider,
        "created_at": user.created_at
    })

