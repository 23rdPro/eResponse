import logging
import os
from .celery import app as celery_app
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logging.basicConfig(filename='appinfo.log', level=logging.DEBUG)


API_SECRET_KEY = os.getenv('API_SECRET_KEY')
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
LOGIN_ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("LOGIN_ACCESS_TOKEN_EXPIRE_MINUTES")

__all__ = (
    'celery_app',
    'oauth2_scheme',
    'pwd_context',
    'ALGORITHM',
    'API_SECRET_KEY',
    'ACCESS_TOKEN_EXPIRE_MINUTES',
    'LOGIN_ACCESS_TOKEN_EXPIRE_MINUTES',

)
