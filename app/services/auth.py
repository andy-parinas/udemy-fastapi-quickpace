from typing import Optional
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from pydantic import BaseModel

from app.settings import settings
from app.models.user import User
from app import repositories as repo
from app.services.security import verify_password
from app.db.session import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1}/auth/login")

class TokenData(BaseModel):
    user_id: Optional[int] = None

def authenticate(*, email: str, password: str, db: Session) -> Optional[User]:
    user = repo.user.get_by_email(db=db, email=email)

    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None

    return user


def create_access_token(*, sub: str) -> str:
    return _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub
    )

def _create_token(token_type: str, lifetime: timedelta, sub: str) -> str:
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload['type'] = token_type

    # https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3
    # The "exp" (expiration time) claim identifies the expiration time on
    # or after which the JWT MUST NOT be accepted for processing
    payload["exp"] = expire

    # The "iat" (issued at) claim identifies the time at which the
    # JWT was issued.
    payload["iat"] = datetime.utcnow()

    # The "sub" (subject) claim identifies the principal that is the
    # subject of the JWT
    payload["sub"] = str(sub)
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)



def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(oauth2_scheme)
) -> User:
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-AUthenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False}
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credential_exception
        token_data = TokenData(user_id=user_id)

    except JWTError:
        raise credential_exception

    user = repo.user.get(db=db, id=token_data.user_id)
    if user is None:
        raise credential_exception
    return user