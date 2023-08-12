import functools
import typing
import uuid
from typing import Annotated, Optional, List

import aiofiles
from fastapi import Depends, File, UploadFile, status, Request
from django.core.files import File as DjangoFile
from django.contrib.auth.models import Group

from starlette.responses import PlainTextResponse, RedirectResponse
from eResponse.response import RESPONSE_PREFIX
from .schemas import (
    EmergencySchema,
    BriefPydanticSchema,
    FileSchema,
    CreateEmergencyPydanticSchema,
    CreateEmergencyResponseSchema,
    UpdateEmergencyResponseSchema,
    UpdateBriefPydanticSchema,
)
from eResponse.user.FastAPI.schemas import GroupSchema, UserSchema
from eResponse.api_helpers import to_schema

from .utils import (
    create_brief_sync,
    aget_or_create,
    create_response_sync,
    transaction_atomic_file,
    get_responses_sync,
    get_emergency_sync,
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


async def oomph(request: Request, user=Depends(get_current_user)):
    req = await request.body()
    await sync_to_async(lambda: print(req))()


async def get_emergency_files(user: Annotated[str, CurrentActiveUser], response_id: str):
    emergency = await get_emergency_sync(response_id)
    files_id = await sync_to_async(lambda: [f.id for b in emergency.briefs.all() for f in b.files.all()])()
    files = await models.File.filters.afilter(id__in=files_id)
    return await sync_to_async(lambda: FileSchema.from_django(files, many=True))()


async def init_response(
        manager: Annotated[str, CurrentActiveUser],
        action: CreateEmergencyResponseSchema = Depends(),
        brief: BriefPydanticSchema = Depends(),
        files: List[UploadFile] = File(...),
):

    b_data_dict = brief.dict()
    b_data = {"title": b_data_dict["brief_title"], "text": b_data_dict["brief_text"], "reporter": manager}
    e_brief = await create_brief_sync(**b_data)

    for file in files:
        async with aiofiles.open(f"eResponse/media/responses/{file.filename}", "wb") as media:
            content = await file.read()
            await media.write(content)

        d_file = models.File()
        await d_file.asave()
        await sync_to_async(lambda: e_brief.files.add(d_file))()

    action_dict = action.dict()

    """
    emergency_type in action_data should be presented in a preset choicefield
    meaning new member is added to the Group type automatically..
    """
    action_data = {
        "emergency_type": await aget_or_create(
            **{"name": action_dict["emergency_type"], "model": Group}
        ),
        "severity": action_dict["severity"],

    }
    response = await create_response_sync(**action_data)

    # add manager: user
    await sync_to_async(lambda: response.respondents.add(manager))()

    # add brief: compulsory
    await sync_to_async(lambda: response.briefs.add(e_brief))()

    await sync_to_async(lambda: print(EmergencySchema.from_orm(response).json()))()

    return await sync_to_async(lambda: EmergencySchema.from_orm(response))()


async def update_response(
        user: Annotated[str, CurrentActiveUser],
        response_id: str,
        file: Optional[UploadFile] = File(None),
        response: UpdateEmergencyResponseSchema = Depends(),
        brief: UpdateBriefPydanticSchema = Depends(),
        additional_file: Optional[UploadFile] = File(None)

):
    e = await Emergency.objects.afilter(id=response_id)

    # update response
    await e.aupdate(**response.dict(exclude_none=True))
    e = await sync_to_async(e.get, thread_sensitive=True)()

    # add brief
    # note: add new brief here* write another view for
    # specific brief update
    b = brief.dict(exclude_none=True)
    if b and ("brief_title" in b and "brief_text" in b):
        b_data = {
            "reporter": user, "title": b['brief_title'],
            "text": b['brief_text']}
        bf = Brief(**b_data)
        await sync_to_async(bf.save)()
        if file is not None:
            async with aiofiles.open(
                    f"eResponse/media/responses/{file.filename}",
                    "wb"
            ) as upload:
                ct = await file.read()
                await upload.write(ct)
            f = models.File()
            await f.asave()
            await sync_to_async(lambda: bf.files.add(f))()
        if additional_file is not None:
            async with aiofiles.open(
                    f"eResponse/media/responses/{additional_file.filename}",
                    "wb"
            ) as upload:
                ct = await additional_file.read()
                await upload.write(ct)
            f = models.File()
            await f.asave()
            await sync_to_async(lambda: bf.files.add(f))()

        await sync_to_async(bf.save)()
        await sync_to_async(lambda: e.briefs.add(bf))()
    await sync_to_async(e.save, thread_sensitive=True)()

    return await EmergencySchema.from_orm(e)


def delete_response():
    pass


async def get_responses(user: Annotated[str, CurrentActiveUser]):
    queryset = await Emergency.filters.aget_all_emergencies()

    if queryset:
        return await to_schema(queryset, EmergencySchema)


def get_response():
    pass
