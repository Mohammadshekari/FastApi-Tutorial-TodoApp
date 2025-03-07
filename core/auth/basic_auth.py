from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session

from core.database import get_db
from users.models import UserModel

security = HTTPBasic()


def get_current_user(
        credentials: HTTPBasicCredentials = Depends(security),
        db: Session = Depends(get_db)):
    user_obj: UserModel | None = db.query(UserModel).filter_by(username=credentials.username).first()
    if not user_obj or not user_obj.verify_password(credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user_obj
