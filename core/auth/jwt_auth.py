from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import DecodeError, InvalidSignatureError

from users.models import UserModel
from core.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt
from core.config import settings

security = HTTPBearer()


def get_authenticated_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
):
    err = "Authentication failed, "
    token = credentials.credentials
    try:
        decoded = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms="HS256")
        user_id = decoded.get('user_id', None)
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=err + "user_id not decoded")
        if decoded.get('type') != 'access':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=err + "invalid token type")
        if datetime.now() > datetime.fromtimestamp(decoded.get('exp')):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=err + "token expired")
        user_obj = db.query(UserModel).filter_by(id=user_id).first()
        return user_obj

    except InvalidSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=err + "invalid signature")
    except DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=err + "decode failed")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=err + str(e))


def generate_access_token(user_id: int, expires_in: int = 60 * 5) -> str:
    now = datetime.utcnow()
    payload = {
        "type": 'access',
        "user_id": user_id,
        "iat": now,
        "exp": now + timedelta(seconds=expires_in)
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")


def generate_refresh_token(user_id: int, expires_in: int = 24 * 3600) -> str:
    now = datetime.utcnow()
    payload = {
        "type": 'refresh',
        "user_id": user_id,
        "iat": now,
        "exp": now + timedelta(seconds=expires_in)
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")
