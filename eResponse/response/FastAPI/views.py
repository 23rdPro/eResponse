from typing import Annotated, Optional, List
from fastapi import Depends, File, UploadFile
from .schemas import EmergencySchema, BriefSchema
from eResponse.user.FastAPI.schemas import GroupSchema
from .utils import start_emergency_sync
from eResponse.response import models
from eResponse import oauth2_scheme
from eResponse.user.FastAPI.views import get_current_user

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
        files: List[UploadFile],
        brief: BriefSchema,
        emergency: EmergencySchema,
        emergency_type: GroupSchema
):
    """
    "however a manager must instantiate this model hence"... from model
    await create brief a must
    then update emergency with stuff
    upload pictures, videos

    permission if user in get_managers

    """
    # print(manager.id, type(manager))
    # print(emergency, type(emergency))
    # await start_emergency_sync(emergency, manager)
    # brief = await create_brief(manager, )
    # picture = await upload_files

    files = [models.File.objects.create(file=file.file) for file in files]

    brief_to_dict = brief.dict()
    brief_data = {"reporter": manager, "title": brief_to_dict.get("title"), "text": brief_to_dict.get("text")}
    brief_instance = models.Brief.objects.create(**brief_data)
    brief_instance.files.add(*files)

    emergency_to_dict = emergency.dict()
    emergency_type_to_dict = emergency_type.dict()

    emergency_data = {"emergency_type": emergency_type_to_dict.get("name"), "severity": emergency_to_dict.get("severity")}
    emergency_instance = models.Emergency.objects.create(**emergency_data)
    emergency_instance.respondents.add(manager)
    emergency_instance.briefs.add(brief_instance)

    "async"


async def create_brief():
    pass


async def get_emergency_response():
    responses = await sync_to_async(lambda: models.Emergency.objects.all())()
    return await sync_to_async(lambda: EmergencySchema.from_django(responses, many=True))()


async def update_response():
    pass


async def delete_response():
    pass

