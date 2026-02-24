from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from apps.db.mongo.connection import db

# Mongo collections
admins_collection = db["superadmins"]
sellers_collection = db["sellers"]


# ===============================
# SUPERADMIN LOGIN
# ===============================
@csrf_exempt
def superadmin_login(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=405)

    data = json.loads(request.body)

    email = data.get("email")
    password = data.get("password")

    admin = admins_collection.find_one({"email": email})

    if not admin or admin["password"] != password:
        return JsonResponse({"error": "Invalid credentials"}, status=401)

    return JsonResponse({
        "message": "Login successful",
        "admin": email
    })

# GET PENDING SELLERS

sellers_collection = db["sellers"]

def get_pending_sellers(request):

    sellers = sellers_collection.find({"status": "pending"})

    data = []

    for s in sellers:
        data.append({
            "id": str(s["_id"]),
            "name": s["full_name"],
            "email": s["email"],
            "status": s["status"]
        })

    return JsonResponse({"sellers": data})
# ===============================
# APPROVE SELLER
# ===============================
@csrf_exempt
def approve_seller(request, seller_id):

    sellers_collection.update_one(
        {"_id": seller_id},
        {
            "$set": {
                "status": "approved",
                "approved_at": datetime.utcnow()
            }
        }
    )

    return JsonResponse({"message": "Seller approved"})