import bcrypt
import jwt
from datetime import datetime, timedelta
from django.conf import settings


def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(
        plain_password.encode(),
        hashed_password.encode()
    )
def create_jwt_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(days=7),  # token expiry
        "iat": datetime.utcnow(),
    }

    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm="HS256"
    )

    return token