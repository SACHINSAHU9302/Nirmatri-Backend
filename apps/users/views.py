import json
import bcrypt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import verify_google_token
from .models import User
from apps.db.mongo.connection import users_collection
from apps.users.utils import create_jwt_token

@csrf_exempt
def user_login(request):
    if request.method == "POST":
        data = json.loads(request.body)

        email = data.get("email")
        password = data.get("password")

        user = users_collection.find_one({"email": email})

        if not user:
            return JsonResponse({"message": "User not found"}, status=404)

        if not bcrypt.checkpw(password.encode(), user["password"].encode()):
            return JsonResponse({"message": "Invalid password"}, status=401)

        token = create_jwt_token(str(user["_id"]))

        return JsonResponse({
            "token": token,
            "user": {
                "id": str(user["_id"]),
                "name": user.get("name"),
                "email": user.get("email"),
                "phone": user.get("phone")
            }
        })

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


# ================= USER LOGIN =================
@csrf_exempt
def user_login(request):
    if request.method == "POST":
        return JsonResponse({"message": "User login API working"})
    return JsonResponse({"error": "Invalid method"}, status=405)


# ================= USER REGISTER =================
@csrf_exempt
def user_register(request):
    if request.method == "POST":
        return JsonResponse({"message": "User register API working"})
    return JsonResponse({"error": "Invalid method"}, status=405)


# ================= FORGOT PASSWORD =================
@csrf_exempt
def forgot_password(request):
    return JsonResponse({"message": "Forgot password API working"})


# ================= RESET PASSWORD =================
@csrf_exempt
def reset_password(request):
    return JsonResponse({"message": "Reset password API working"})