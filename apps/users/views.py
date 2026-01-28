import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import verify_google_token
from .models import User

@csrf_exempt
def google_login(request):
    if request.method == "OPTIONS":
        return JsonResponse({}, status=200)

    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        body = json.loads(request.body)
        token = body.get("token")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    if not token:
        return JsonResponse({"error": "Token missing"}, status=400)

    data = verify_google_token(token)

    user, _ = User.objects.get_or_create(
        email=data["email"],
        defaults={
            "name": data["name"],
            "picture": data.get("picture", "")
        }
    )

    request.session["user_id"] = str(user.id)
    request.session.set_expiry(60 * 60 * 24)

    return JsonResponse({
        "message": "Login successful",
        "email": user.email
    })
