from apps.users.googleauth.services import verify_google_token, get_or_create_google_user
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.conf import settings
from apps.db.mongo.connection import users_collection
from datetime import datetime, timedelta
import jwt




@api_view(["POST"])
def google_login(request):
    token = request.data.get("token")

    idinfo = verify_google_token(token)

    if not idinfo:
        return Response({"error": "Invalid token"}, status=400)

    user, created = get_or_create_google_user(idinfo)

    # Save in MongoDB
    mongo_user = users_collection.find_one({"email": user.email})

    if not mongo_user:
        result = users_collection.insert_one({
            "name": user.name,
            "email": user.email,
            "mobile": "",
            "gender": "",
            "auth_provider": "google",
            "is_active": True
        })

        mongo_id = str(result.inserted_id)
    else:
        mongo_id = str(mongo_user["_id"])

    # Create JWT using MongoDB id
    payload = {
        "user_id": mongo_id,
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(days=7),
        "iat": datetime.utcnow(),
    }

    jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    return Response({
        "token": jwt_token,
        "user": {
            "id": mongo_id,
            "email": user.email,
            "name": user.name,
            "mobile": "",
            "gender": "",
            "is_active": True
        }
    })



