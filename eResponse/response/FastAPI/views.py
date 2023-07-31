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
    create_brief_sync,
    aget_or_create,
    create_response_sync,
    transaction_atomic_file,
    get_responses_sync,
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
        async with aiofiles.open(f"eResponse/media/responses/{file.filename}", "wb") as media:
            content = await file.read()
            await media.write(content)
        b_file = await transaction_atomic_file()
        await sync_to_async(lambda: e_brief.files.add(b_file))()

    action_dict = action.dict()
    action_data = {
        "emergency_type": await aget_or_create(
            **{"name": action_dict["emergency_type"], "model": Group}
        ),
        "severity": action_dict["severity"],

    }
    response = await create_response_sync(**action_data)
    await sync_to_async(lambda: response.respondents.add(manager))()
    await sync_to_async(lambda: response.briefs.add(e_brief))()

    return await to_schema(response, EmergencySchema)


async def update_response(
        user: Annotated[str, CurrentActiveUser],
        response_id: str,
        response: CreateEmergencyResponseSchema = Depends(),
        files: List[UploadFile] = File(...),

):
    response = await Emergency.objects.aget(id=response_id)
    r_schema = await to_schema(response, EmergencySchema)

    r_data = response.dict(exclude_unset=True)
    r_update = response.copy(update=r_data)

    return r_update
    # await run_model_update(**{"model": Emergency, })


def delete_response():
    pass


async def get_responses(user: Annotated[str, CurrentActiveUser]):
    # files = await sync_to_async(lambda: models.File.objects.all())()
    # # await sync_to_async(lambda: print(files))()
    # async for file in files:
    #     await sync_to_async(lambda: print(file, file.file))()

    # return await to_schema(files, FileSchema)

    ids = []
    responses = await get_responses_sync()
    # async for response in responses:
    #     async for brief in response.briefs:
    #         file = brief.

    # await sync_to_async(lambda: print(len(responses), len(_responses)))()

    # return await to_schema(responses, EmergencySchema)



def get_response():
    pass



