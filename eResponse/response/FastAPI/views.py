from fastapi import Depends
from eResponse.user.FastAPI.views import get_current_active_user
from .schemas import EmergencySchema
from .utils import start_emergency_sync
from eResponse.response import models

from asgiref.sync import sync_to_async

CurrentUser = Depends(get_current_active_user)


async def start_emergency_response(*, manager: CurrentUser, emergency: EmergencySchema):
    response = await start_emergency_sync(**emergency.dict())
    return emergency


async def get_emergency_response():
    responses = await sync_to_async(lambda: models.Emergency.objects.all())()
    return await sync_to_async(lambda: EmergencySchema.from_django(responses, many=True))()


async def update_response():
    pass


async def delete_response():
    pass

