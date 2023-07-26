from typing import Annotated, Optional, List
from fastapi import Depends, File, UploadFile, status
from starlette.responses import PlainTextResponse, RedirectResponse
from eResponse.response import RESPONSE_PREFIX
from .schemas import EmergencySchema, BriefSchema, FileSchema
from eResponse.user.FastAPI.schemas import GroupSchema
from .utils import start_emergency_sync, start_emergency_sync, is_user_manager
from eResponse.response import models
from eResponse import oauth2_scheme, PREFIX
from eResponse.user.FastAPI.views import get_current_user
from eResponse.user.models import User
# from eResponse.response.models import Emergency, Brief, File

from asgiref.sync import sync_to_async

from eResponse.response.models import Emergency, Brief

CurrentUser = Depends(oauth2_scheme)
CurrentActiveUser = Depends(get_current_user)

"""
router.post("/ers-files/{user_id}/{mime_type}", )  # create_file
router.post("/ers-files/upload/file", )  # upload file

"""


async def start_emergency_response(
        *, manager: Annotated[str, CurrentActiveUser],
        emergency: EmergencySchema,
        emergency_type: GroupSchema
):

    emergency_type_to_dict = emergency_type.dict()  # Group
    emergency_to_dict = emergency.dict()
    emergency_data = {"emergency_type": emergency_type_to_dict.get("name"),
                      "severity": emergency_to_dict.get("severity")}
    emergency_instance = Emergency.objects.create(**emergency_data)

    # however a manager must instantiate this model hence"... from model
    emergency_instance.respondents.add(manager)
    # respondents cannot be blank, but because we need to wait for files
    # before creating emergency leading to response redirect after successive segments:
    # we made briefs accept blank in model to allow us ultimately call save() on emergency

    emergency_instance.save()

    return RedirectResponse(url=f"{PREFIX}/{RESPONSE_PREFIX}/add-brief/{str(emergency_instance.id)}/{str(manager.id)}",
                            status_code=status.HTTP_307_TEMPORARY_REDIRECT)


async def create_brief(emergency_id: str, brief: BriefSchema, user_id: str):
    emergency = Emergency.objects.get(emergency_id)
    user = User.objects.get(user_id)

    brief_to_dict = brief.dict()
    brief_data = {"reporter": user, "title": brief_to_dict.get("title"), "text": brief_to_dict.get("text")}
    brief_instance = Brief.objects.create(**brief_data)

    emergency.briefs.add(brief_instance)
    emergency.save()

    return RedirectResponse(url=f"{PREFIX}/{RESPONSE_PREFIX}/add-files/{str(emergency.id)}",
                            status_code=status.HTTP_307_TEMPORARY_REDIRECT)


async def upload_files(files: List[UploadFile], emergency_id: str)


async def get_emergency_response():
    responses = await sync_to_async(lambda: models.Emergency.objects.all())()
    return await sync_to_async(lambda: EmergencySchema.from_django(responses, many=True))()


async def update_response():
    pass


async def delete_response():
    pass

