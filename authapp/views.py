import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password

from apps.db.mongo.collections import users_collection


# 🔹 ROOT / HOME VIEW
def home(request):
    return JsonResponse({
        "status": "Backend running successfully 🚀",
        "message": "Django + MongoDB connected"
    })


# 🔹 REGISTER API
@csrf_exempt
def register(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Only POST method allowed"},
            status=405
        )

    try:
        data = json.loads(request.body)

        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        password = data.get("password")

        # ❌ VALIDATION
        if not all([first_name, last_name, email, password]):
            return JsonResponse(
                {"error": "All fields are required"},
                status=400
            )

        # ❌ Email already exists
        if users_collection.find_one({"email": email}):
            return JsonResponse(
                {"error": "Email already registered"},
                status=400
            )

        # ✅ SAVE USER
        user = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": make_password(password),
            "role": "user",
            "is_active": True
        }

        users_collection.insert_one(user)

        return JsonResponse(
            {"message": "User registered successfully"},
            status=201
        )

    except Exception as e:
        return JsonResponse(
            {"error": str(e)},
            status=500
        )


# 🔹 LOGIN API (OPTIONAL BUT READY)
@csrf_exempt
def login(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method allowed"}, status=405)

    data = json.loads(request.body)

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return JsonResponse({"error": "Email and password required"}, status=400)

    user = users_collection.find_one({"email": email})

    if not user or not check_password(password, user["password"]):
        return JsonResponse({"error": "Invalid credentials"}, status=401)

    return JsonResponse({
        "message": "Login successful",
        "user": {
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "email": user["email"],
            "role": user["role"]
        }
    })
