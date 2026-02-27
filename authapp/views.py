import json
import secrets
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings

from apps.db.mongo import users_collection
from apps.db.mongo.db_collections import sellers_collection
from .utils import (
    hash_password,
    check_password,
    generate_reset_token,
    token_expiry
)

# ===============================
# ROOT / HEALTH CHECK
# ===============================
def home(request):
    return JsonResponse({
        "status": "Backend running successfully 🚀",
        "message": "Django + MongoDB connected"
    })


# ===============================
# REGISTER API
# ===============================
@csrf_exempt
def register(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method allowed"}, status=405)

    try:
        data = json.loads(request.body)

        first_name = data.get("firstName")
        last_name = data.get("lastName")
        email = data.get("email")
        password = data.get("password")

        if not all([first_name, last_name, email, password]):
            return JsonResponse({"error": "All fields are required"}, status=400)

        email = email.lower()

        if users_collection.find_one({"email": email}):
            return JsonResponse({"error": "Email already registered"}, status=400)

        from datetime import datetime

        user = {
            "firstName": first_name,   # 🔥 camelCase
            "lastName": last_name,
            "email": email,
            "password": hash_password(password),
            "phone": "",               # default empty (important)
            "gender": "",
            "role": "user",
            "is_active": True,
            "created_at": datetime.utcnow()
        }

        users_collection.insert_one(user)

        return JsonResponse(
            {"message": "User registered successfully"},
            status=201
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# ===============================
# LOGIN API (TOKEN BASED)
# ===============================
@csrf_exempt
def login(request):
    
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method allowed"}, status=405)

    try:
        print("🔵 LOGIN API HIT")

        data = json.loads(request.body)
        print("📦 DATA:", data)

        email = data.get("email")
        password = data.get("password")

        print("📧 EMAIL:", email)
        print("🔑 PASSWORD:", password)

        if not email or not password:
            return JsonResponse(
                {"error": "Email and password required"},
                status=400
            )

        email = email.lower()
        print("📧 EMAIL LOWER:", email)

        user = users_collection.find_one({"email": email})
        print("👤 USER FOUND:", user)

        if not user:
            return JsonResponse(
                {"error": "Invalid email or password"},
                status=401
            )

        if not check_password(password, user["password"]):
            return JsonResponse(
                {"error": "Invalid email or password"},
                status=401
            )

        print("✅ PASSWORD MATCHED")

        token = secrets.token_hex(32)
        expiry = datetime.utcnow() + timedelta(days=7)

        print("🔐 TOKEN GENERATED")

        users_collection.update_one(
            {"_id": user["_id"]},
            {
                "$set": {
                    "auth_token": token,
                    "token_expiry": expiry
                }
            }
        )

        print("💾 TOKEN SAVED")

        return JsonResponse({
            "message": "Login successful",
            "token": token,
            "user": {
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "email": user["email"],
                "role": user.get("role", "user")
            }
        }, status=200)

    except Exception as e:
        print("❌ LOGIN CRASH ERROR 👉", repr(e))
        import traceback
        traceback.print_exc()
        return JsonResponse({"error": "Login failed"}, status=500)
    
    from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



# ===============================
# FORGOT PASSWORD
# ===============================
@csrf_exempt
def forgot_password(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    try:
        data = json.loads(request.body)
        email = data.get("email")

        if not email:
            return JsonResponse({"error": "Email required"}, status=400)

        email = email.lower()
        user = users_collection.find_one({"email": email})

        if not user:
            return JsonResponse({"error": "User not found"}, status=404)

        reset_token = generate_reset_token()
        expiry = token_expiry()

        users_collection.update_one(
            {"_id": user["_id"]},
            {
                "$set": {
                    "reset_token": reset_token,
                    "reset_token_expiry": expiry
                }
            }
        )

        reset_link = f"http://localhost:3000/userauth/reset-password?token={reset_token}"

        send_mail(
            subject="Reset your Nirmatri password",
            message=(
                "Click the link below to reset your password:\n\n"
                f"{reset_link}\n\n"
                "This link expires in 15 minutes."
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )

        return JsonResponse(
            {"message": "Password reset link sent"},
            status=200
        )

    except Exception:
        return JsonResponse({"error": "Failed to send reset email"}, status=500)


# ===============================
# RESET PASSWORD
# ===============================
@csrf_exempt
def reset_password(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    try:
        data = json.loads(request.body)

        token = data.get("token")
        new_password = data.get("new_password")

        if not token or not new_password:
            return JsonResponse(
                {"error": "Token and new password required"},
                status=400
            )

        user = users_collection.find_one({
            "reset_token": token,
            "reset_token_expiry": {"$gt": datetime.utcnow()}
        })

        if not user:
            return JsonResponse(
                {"error": "Invalid or expired token"},
                status=400
            )

        users_collection.update_one(
            {"_id": user["_id"]},
            {
                "$set": {"password": hash_password(new_password)},
                "$unset": {
                    "reset_token": "",
                    "reset_token_expiry": ""
                }
            }
        )

        return JsonResponse(
            {"message": "Password reset successful"},
            status=200
        )

    except Exception:
        return JsonResponse({"error": "Password reset failed"}, status=500)

@csrf_exempt
def login(request):
    return JsonResponse({"message": "LOGIN API HIT"}, status=200)
