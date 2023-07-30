from typing import Annotated, Optional, List

import aiofiles
from fastapi import Depends, File, UploadFile, status
from django.core.files import File as DjangoFile
from django.contrib.auth.models import Group

from starlette.responses import PlainTextResponse, RedirectResponse
from eResponse.response import RESPONSE_PREFIX
from .schemas import (
    EmergencySchema,
    BriefSchema,
    FileSchema,
    CreateEmergencyPydanticSchema,
    CreateEmergencyResponseSchema,
)
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
    create_file_sync,
    get_model_object,
    create_response_sync,
    transaction_atomic_file
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


async def init_response(
        manager: Annotated[str, CurrentActiveUser],
        action: CreateEmergencyResponseSchema = Depends(),
        brief: BriefSchema = Depends(),
        files: List[UploadFile] = File(...),
):

    b_data_dict = brief.dict()
    b_data = {"title": b_data_dict["title"], "text": b_data_dict["text"], "reporter": manager}
    e_brief = await create_brief_sync(**b_data)

    for file in files:
        async with aiofiles.open(f"eResponse/media/{file.filename}", "wb") as media:
            content = await file.read()
            await media.write(content)
        b_file = await transaction_atomic_file()
        await sync_to_async(lambda: e_brief.files.add(b_file))()

    action_dict = action.dict()
    action_data = {
        "emergency_type": await get_model_object(
            **{"name": action_dict["emergency_type"], "model": Group}
        ),
        "severity": action_dict["severity"],

    }
    response = await create_response_sync(**action_data)
    await sync_to_async(lambda: response.respondents.add(manager))()
    await sync_to_async(lambda: response.briefs.add(e_brief))()

    return await to_schema(response, EmergencySchema)


def update_response(
        user: Annotated[str, CurrentActiveUser],

):
    pass


def delete_response():
    pass


def get_responses():
    pass


def get_response():
    pass



