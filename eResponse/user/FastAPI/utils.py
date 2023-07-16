from __future__ import annotations

from datetime import timedelta, datetime
from asgiref.sync import sync_to_async
from jose import jwt, JWTError
from eResponse import oauth2_scheme, pwd_context, ALGORITHM, API_SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES


@sync_to_async
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta is not None:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, API_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
