import os

from django.core.wsgi import get_wsgi_application
from fastapi import FastAPI

from eResponse.user.FastAPI.urls import router

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eResponse.settings')

application = get_wsgi_application()

app = FastAPI(
    title="Emergency Response App",
    description="",
    version="",
)

app.include_router(router=router, prefix='/v1')
