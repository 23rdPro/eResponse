import os
import django

from django.core.wsgi import get_wsgi_application
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

django.setup()

from .urls import router  # noqa: E402

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eResponse.settings')

# os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"  todo: safe?

application = get_wsgi_application()

app = FastAPI(
    title="Emergency Response App",
    description="",
    version="1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=router, prefix='/api/v1')

