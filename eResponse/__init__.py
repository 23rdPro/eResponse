import logging
from .celery import app as celery_app
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")
logging.basicConfig(filename='appinfo.log', level=logging.DEBUG)

__all__ = ('celery_app', 'oauth2_scheme')
