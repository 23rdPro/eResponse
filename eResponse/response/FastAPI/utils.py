from typing import Optional, List
from asgiref.sync import sync_to_async
from django.contrib.auth.models import Group
from fastapi import UploadFile
from eResponse.response.models import Emergency, Brief, File
from djantic.main import ModelSchema
from eResponse.user.models import User


@sync_to_async
def decode_token(user):
    pass


@sync_to_async
def is_user_manager(user: User):
    return user in User.filters.get_managers()


@sync_to_async
def start_emergency_sync(manager: User, files: List[UploadFile],
                         brief: ModelSchema, emergency: ModelSchema,
                         emergency_type: ModelSchema):

    files = [File.objects.create(file=file.file) for file in files]

    brief_to_dict = brief.dict()
    brief_data = {"reporter": manager, "title": brief_to_dict.get("title"), "text": brief_to_dict.get("text")}
    brief_instance = Brief.objects.create(**brief_data)
    brief_instance.files.add(*files)

    emergency_to_dict = emergency.dict()
    emergency_type_to_dict = emergency_type.dict()

    emergency_data = {"emergency_type": emergency_type_to_dict.get("name"), "severity": emergency_to_dict.get("severity")}
    emergency_instance = Emergency.objects.create(**emergency_data)

    emergency_instance.respondents.add(manager)
    emergency_instance.briefs.add(brief_instance)
    return emergency_instance

    # pass
    # print(Emergency.objects.filter(id=schema.dict().get(id)))
    # print(Emergency.objects.all())
    # await sync_to_async(lambda: print(Emergency.objects.filter(id=schema.get(id))))()
    # emergency = Emergency.objects.get_or_create(schema.get(id))

    # assert manager.id in list(d['id'] for d in schema.get("respondents"))

    # _new = {}
    # emergency_type = respondents = briefs = None
    #
    # for field in schema:
    #     if field == "emergency_type":
    #         emergency_type = Group.objects.get(name=schema.get(field))
    #     elif field == "respondents":
    #         respondents = [User.objects.get(id=respondent.get(id))
    #                        for respondent in schema.get(field)]
    #     elif field == "briefs":
    #         briefs = [Brief.objects.get(id=brief.get(id))
    #                   for brief in schema.get(field)]
    #     else:
    #         _new.update(dict([(field, schema.get(field))]))
    #
    # emergency = Emergency(**_new)
    # emergency.save()
    # emergency.emergency_type.add(emergency_type)
    # emergency.respondents.add(*respondents)
    # emergency.briefs.add(*briefs)


@sync_to_async
def create_brief():
    pass
