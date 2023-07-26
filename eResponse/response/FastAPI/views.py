from typing import Annotated, Optional, List
from fastapi import Depends, File, UploadFile, status
from starlette.responses import PlainTextResponse, RedirectResponse
from eResponse.response import RESPONSE_PREFIX
from .schemas import EmergencySchema, BriefSchema, FileSchema, StartEmergencySchema
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


async def create_emergency_response(emg: EmergencySchema, manager: Annotated[str, CurrentActiveUser],
                                    header: Annotated[str, Depends(application_vnd)],
                                    files: List[UploadFile], briefs: List[BriefSchema],
                                    respondents: List[UserSchema], emergency_type: GroupSchema):

    briefs_objs = await create_briefs_sync(briefs)
    async for brief in briefs_objs:
        files_objs = await create_files_sync(files, brief)

    group = await create_emergency_type_sync(emergency_type)
    users = await create_respondents_sync(respondents, manager)
    emergency = await create_emergency_sync(group, users, briefs, emg)


async def start_emergency_response(
        *, manager: Annotated[str, CurrentActiveUser],
        emergency: StartEmergencySchema,
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


async def upload_files(files: List[UploadFile], emergency_id: str):
    _data = {"files": files, "emergency_id": emergency_id}
    file_instance: Emergency = await upload_files_sync(**_data)

    return await to_schema(file_instance, EmergencySchema)


async def get_emergency_response():
    responses = await sync_to_async(lambda: models.Emergency.objects.all())()
    return await sync_to_async(lambda: EmergencySchema.from_django(responses, many=True))()


async def update_response():
    pass


async def delete_response():
    pass

