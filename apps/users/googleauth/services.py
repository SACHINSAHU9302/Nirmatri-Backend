from apps.users.models import GoogleUser


def verify_google_token(token):
    from google.oauth2 import id_token
    from google.auth.transport import requests
    from django.conf import settings

    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )

        print("✅ Token verified successfully")
        return idinfo

    except Exception as e:
        print("❌ Token verification failed:", str(e))
        return None


def get_or_create_google_user(idinfo):
    """
    Create user if not exists, otherwise return existing user
    """

    email = idinfo.get("email")
    name = idinfo.get("name")
    picture = idinfo.get("picture")

    user, created = GoogleUser.objects.get_or_create(
        email=email,
        defaults={
            "name": name,
            "picture": picture
        }
    )

    return user, created