import json
import bcrypt
import jwt

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from apps.db.mongo.connection import users_collection
from apps.users.utils import create_jwt_token


# ================= USER LOGIN =================
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

    return JsonResponse({"error": "Invalid method"}, status=405)


# ================= GET PROFILE =================
@csrf_exempt
def get_profile(request):

    try:
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return JsonResponse({"error": "Token missing"}, status=401)

        token = auth_header.split(" ")[1]

        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = decoded.get("user_id")

        user = users_collection.find_one({"_id": user_id})

        if not user:
            return JsonResponse({"error": "User not found"}, status=404)

        return JsonResponse({
            "id": str(user["_id"]),
            "name": user.get("name"),
            "email": user.get("email"),
            "phone": user.get("phone"),
            "gender": user.get("gender"),
            "firstName": user.get("firstName"),
            "lastName": user.get("lastName"),
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ================= UPDATE PROFILE =================
@csrf_exempt
def update_profile(request):

    if request.method == "PUT":

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return JsonResponse({"error": "Token missing"}, status=401)

        token = auth_header.split(" ")[1]

        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = decoded.get("user_id")

        data = json.loads(request.body)

        users_collection.update_one(
            {"_id": user_id},
            {"$set": data}
        )

        return JsonResponse({"message": "Profile updated successfully"})

    return JsonResponse({"error": "Invalid method"}, status=405)


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