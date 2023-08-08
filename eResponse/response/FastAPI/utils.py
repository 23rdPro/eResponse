import uuid
from typing import Optional, List
from asgiref.sync import sync_to_async
from django.contrib.auth.models import Group
from django.db import transaction
from fastapi import UploadFile, Header, HTTPException, status
from eResponse.response.models import Emergency, Brief, File
from django.core.files.base import File as DjangoFile
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


@sync_to_async
def create_brief():
    pass


@sync_to_async
def start_emergency_response_sync(**kwargs):
    emergency_to_dict = kwargs.get("emergency").dict()
    emergency_data = {
        "emergency_type": Group.objects.get_or_create(
            emergency_to_dict.get("emergency_type").get("name"))[0],

        "severity": emergency_to_dict.get("severity")
    }
    emergency_instance = Emergency.objects.create(**emergency_data)

    # however a manager must instantiate this model hence"... from model
    emergency_instance.respondents.add(kwargs.get("manager"))
    # respondents cannot be blank, but because need to wait for files before
    # creating emergency leading to response redirect after successive segments:
    # made briefs accept blank in model to allow us ultimately call save() on emergency

    emergency_instance.save()
    return emergency_instance


@sync_to_async
def create_brief_sync(**kwargs):
    return Brief.objects.create(**kwargs)


@sync_to_async
def create_emergency_group_sync(name: str):
    return Group.objects.get_or_create(name)[0]


@sync_to_async
def upload_files_sync(**kwargs):
    file_objs = File.objects.bulk_create([File(file=file.file) for file in kwargs.get("files")])
    emergency = Emergency.objects.get(id=kwargs.get("emergency_id"))
    print("this field_names>>>>>>>", emergency.field_names, type(emergency.field_names))
    briefs = emergency.briefs.all()
    if briefs.count() == 1:
        brief = briefs.get()
        brief.files.add(*file_objs)
        brief.save()
    else:
        pass  # todo

    emergency.save()
    return emergency


def application_vnd(content_type: str = Header(...)):
    """Require request MIME-type to be application/vnd.api+json"""

    if content_type != "application/vnd.api+json":
        raise HTTPException(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Unsupported media type: {content_type}."
            " It must be application/vnd.api+json",
        )


@sync_to_async
def create_files_sync(files: List[str],):
    filez = []
    for name in files:
        with open(name) as fx:
            fz = File()
            field_file = DjangoFile(fx)
            fz.file.save(field_file.name, field_file)
            filez.append(fz)
    return filez


@sync_to_async
def create_emergency_response_sync(e_data: dict, brief: Brief, user: User):
    emergency = Emergency.objects.create(**e_data)
    emergency.respondents.add(user)
    emergency.briefs.add(brief)
    emergency.save()
    return emergency


@sync_to_async
def create_file_sync(path: str):
    with open(path) as MEDIA:
        file = File()
        d_type = DjangoFile(MEDIA)
        file.file.save('media', d_type)
        file.save()
    return file


@sync_to_async
def aget_or_create(**kwargs):
    model = kwargs.pop("model")
    return model.objects.get_or_create(**kwargs)[0]


@sync_to_async
def create_response_sync(**kwargs):
    return Emergency.objects.create(**kwargs)


@sync_to_async
@transaction.atomic
def transaction_atomic_file():
    d_file = File()
    d_file.save()  # noqa
    return d_file


@sync_to_async
def get_responses_sync():
    return Emergency.filters.get_all_emergencies()


@sync_to_async
def get_emergency_sync(e_id: str):
    queryset = Emergency.filters.get_all_emergencies().filter(id=e_id)
    if queryset.exists():
        return queryset.get()
    return
