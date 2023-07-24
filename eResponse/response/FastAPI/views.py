from typing import Annotated
from fastapi import Depends
from .schemas import EmergencySchema
from .utils import start_emergency_sync
from eResponse.response import models
from eResponse import oauth2_scheme
from eResponse.user.FastAPI.views import get_current_user

from asgiref.sync import sync_to_async

from eResponse.response.models import Emergency, Brief

CurrentUser = Depends(oauth2_scheme)
CurrentActiveUser = Depends(get_current_user)


async def start_emergency_response(*, manager: Annotated[str, CurrentActiveUser], emergency: EmergencySchema):
    """
    "however a manager must instantiate this model hence"... from model
    :param manager:
    :param emergency:
    :return:
    """
    # print(manager.id, type(manager))
    # print(emergency, type(emergency))
    await start_emergency_sync(emergency, manager)




async def create_brief():
    pass


async def get_emergency_response():
    responses = await sync_to_async(lambda: models.Emergency.objects.all())()
    return await sync_to_async(lambda: EmergencySchema.from_django(responses, many=True))()


async def update_response():
    pass


async def delete_response():
    pass

