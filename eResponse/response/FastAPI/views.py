from typing import Annotated, Optional, List
from fastapi import Depends, File, UploadFile, status
from django.contrib.auth.models import Group
from django.db import transaction
from starlette.responses import PlainTextResponse, RedirectResponse
from eResponse.response import RESPONSE_PREFIX
from .schemas import EmergencySchema, BriefSchema, FileSchema, CreateEmergencyPydanticSchema
from eResponse.user.FastAPI.schemas import GroupSchema, UserSchema
from eResponse.api_helpers import to_schema

from .utils import (
    start_emergency_sync,
    start_emergency_sync,
    is_user_manager,
    start_emergency_response_sync,
    create_brief_sync,
    upload_files_sync,
    application_vnd,
    create_files_sync,
    create_emergency_response_sync,
    create_emergency_group_sync,
    schema_to_dict,
    brief_data_from_e_dict_sync,
)
from eResponse.response import models
from eResponse import oauth2_scheme, PREFIX
from eResponse.user.FastAPI.views import get_current_user
from eResponse.user.models import User
# from eResponse.response.models import Emergency, Brief, File

from asgiref.sync import sync_to_async

from eResponse.response.models import Emergency, Brief

CurrentUser = Depends(oauth2_scheme)
CurrentActiveUser = Depends(get_current_user)


async def create_emergency_response(
        manager: Annotated[str, CurrentActiveUser],
        emg: CreateEmergencyPydanticSchema
):
    # pass
    await sync_to_async(lambda: print(emg))()
    return emg
    # filez: list = await create_files_sync(files)
    # print(filez)
    #
    # emg_dict = await schema_to_dict(emg)
    #
    # brief_data = await brief_data_from_e_dict_sync(emg_dict, manager)
    # brief = await create_brief_sync(filez, brief_data)
    #
    # group_name = await sync_to_async(lambda: emg_dict.get("emergency_type").get("name"))()
    # emergency_group = await create_emergency_group_sync(group_name)
    #
    # severity = await sync_to_async(lambda: emg_dict.get("severity"))()
    # emergency_data = {"emergency_type": emergency_group, "severity": severity}
    #
    # emergency = await create_emergency_response_sync(emergency_data, brief, manager)
    #
    # return await to_schema(emergency, EmergencySchema)


async def upload_files(files: List[UploadFile], emergency_id: str):
    emergency = await create_files_sync(files, emergency_id)
    return await to_schema(emergency, EmergencySchema)


async def start_emergency_response(
        *, manager: Annotated[str, CurrentActiveUser],
        emergency: Emergency,
        # emergency_type: GroupSchema
):
    _data = {"manager": manager, "emergency": emergency}  # "emergency_type": emergency_type
    emergency_instance = await start_emergency_response_sync(**_data)

    return RedirectResponse(url=f"{PREFIX}/{RESPONSE_PREFIX}/add-brief/{emergency_instance.id}/{manager.id}",
                            )


async def create_brief(emergency_id: str, user_id: str, brief: Annotated[str, BriefSchema]):
    await sync_to_async(lambda: print(emergency_id))()
    _data = {"emergency_id": emergency_id, "brief": brief, "user_id": user_id}
    brief_instance: Emergency = await create_brief_sync(**_data)

    return RedirectResponse(url=f"{PREFIX}/{RESPONSE_PREFIX}/add-files/{str(brief_instance.id)}",
                            status_code=status.HTTP_307_TEMPORARY_REDIRECT)


# async def upload_files(files: List[UploadFile], emergency_id: str):
#     _data = {"files": files, "emergency_id": emergency_id}
#     file_instance: Emergency = await upload_files_sync(**_data)
#
#     return await to_schema(file_instance, EmergencySchema)


async def get_emergency_response():
    responses = await sync_to_async(lambda: models.Emergency.objects.all())()
    return await sync_to_async(lambda: EmergencySchema.from_django(responses, many=True))()


async def update_response():
    pass


async def delete_response():
    pass

