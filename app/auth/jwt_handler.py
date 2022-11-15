import time
import jwt
from decouple import config

JWT_SECRET = config("secret")
JWT_ALGORITHM = config("algorithm")


# Sign JWT
def signJWT(email: str, duration: int = 3600, type: int = 1): # 3600 seconds = 1 hour
    payload = {
        "email": email,
        "iat": time.time(),
        "exp": time.time() + duration,
        "type": type
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {
        "access_token": token,
    }


# Verify JWT
def decodeJWT(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        return payload if payload['exp'] > time.time() else None
    except:
        return None
