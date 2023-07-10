from .celery import app as celery_app
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

__all__ = ('celery_app', 'oauth2_scheme')
