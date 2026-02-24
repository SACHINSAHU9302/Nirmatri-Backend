#Seller Register API
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
# ...existing code...
# replace:
from apps.db.mongo import sellers_collection
# with:
from apps.db.mongo.db_collections import sellers_collection
# ...existing code...
from datetime import datetime
from .services import seller_login
from .services import seller_login_service


#register API

@csrf_exempt
@require_POST
def seller_register(request):
    try:
        data = json.loads(request.body)

        full_name = data.get("full_name")
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        # ================= VALIDATION =================
        missing = []
        for field in ["full_name", "email", "password", "confirm_password"]:
            if not data.get(field):
                missing.append(field)

        if missing:
            return JsonResponse(
                {"error": "Missing fields", "fields": missing},
                status=400
            )

        if password != confirm_password:
            return JsonResponse(
                {"error": "Passwords do not match"},
                status=400
            )

        # ================= DUPLICATE CHECK =================
        if sellers_collection.find_one({"email": email}):
            return JsonResponse(
                {"error": "Seller already registered with this email"},
                status=409
            )

        # ================= SAVE TO DB =================
        seller_doc = {
            "full_name": full_name,
            "email": email,
            "password": password,  # 🔒 Later hash karenge
            "status": "pending",   # 👈 SUPERADMIN APPROVAL
            "created_at": datetime.utcnow(),
            "approved_at": None,
            "approved_by": None
        }

        sellers_collection.insert_one(seller_doc)

        return JsonResponse(
            {
                "message": "Seller registered successfully",
                "status": "pending",
                "note": "Your account will be activated after admin approval"
            },
            status=201
        )

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    except Exception as e:
        print("SELLER REGISTER ERROR:", str(e))
        return JsonResponse(
            {"error": "Server error", "details": str(e)},
            status=500
        )

#seller onboarding API

@csrf_exempt
def seller_onboarding(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        data = json.loads(request.body)

        seller_doc = {
            # STORE INFO
            "owner_name": data.get("ownerName"),
            "store_name": data.get("storeName"),
            "store_category": data.get("storeCategory", []),

            # KYC
            "pan_number": data.get("panNumber"),
            "aadhaar_number": data.get("aadhaarNumber"),

            # BANK
            "account_holder": data.get("accountHolderName"),
            "account_number": data.get("accountNumber"),
            "ifsc_code": data.get("ifscCode"),
            "bank_name": data.get("bankName"),

            # PHONE
            "phone_number": data.get("phoneNumber"),

            # STATUS
            "status": "pending",
            "created_at": datetime.utcnow(),
        }

        sellers_collection.insert_one(seller_doc)

        return JsonResponse({
            "message": "Seller onboarding completed",
            "status": "pending_approval"
        }, status=201)

    except Exception as e:
        return JsonResponse({
            "error": str(e)
        }, status=500)
    

#seller login API

@csrf_exempt
def seller_login(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=405)

    try:
        data = json.loads(request.body)

        response, status = seller_login_service(data)

        return JsonResponse(response, status=status)

    except Exception as e:
        return JsonResponse(
            {"error": str(e)},
            status=500
        )