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


@sync_to_async
def start_emergency_response_sync(**kwargs):
    # emergency_type_to_dict = kwargs.get("emergency_type").dict()  # Group
    emergency_to_dict = kwargs.get("emergency").dict()
    emergency_data = {
        "emergency_type": Group.objects.get_or_create(
            emergency_to_dict.get("emergency_type").get("name"))[0],

        "severity": emergency_to_dict.get("severity")
    }
    emergency_instance = Emergency.objects.create(**emergency_data)

    # however a manager must instantiate this model hence"... from model
    emergency_instance.respondents.add(kwargs.get("manager"))
    # respondents cannot be blank, but because we need to wait for files
    # before creating emergency leading to response redirect after successive segments:
    # we made briefs accept blank in model to allow us ultimately call save() on emergency

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

    #         my_file.save()
    #         # await sync_to_async(lambda: my_file.save())()
    #         filez.append(my_file)
    # return filez

    #         filez.append(File(file=DjangoFile(fx)))
    # filez = File.objects.bulk_create(*filez)
    # return filez

    # filez = []
    # for file_path in files:
    #     with open(file_path, 'r') as file:
    #         filez.append(File.objects.create(file=file))
    # return filez

    # print(files, ">>>>>>>>>>>>>>>>>>>>>>>.")
    # # for f in files:
    #     # print(f.read())
    #     # print(f.filename, type(f.file), f.size)
    #     # with open(f.filename, 'r') as fg:
    #     #     print(fg.readlines())
    #     # print(dir(f.file))
    # filez = File.objects.bulk_create([file.file for file in files])
    # print(type(filez), "files_obj>>>>>>>>>>>>>")
    # return filez
    # emergency = Emergency.objects.get(id=emergency_id)
    # emergency.briefs.files.add(*filez)
    # emergency.save()
    # return emergency


@sync_to_async
def create_emergency_response_sync(e_data: dict, brief: Brief, user: User):
    emergency = Emergency.objects.create(**e_data)
    emergency.respondents.add(user)
    emergency.briefs.add(brief)
    emergency.save()
    return emergency

    # emergency_type = Group.objects.get_or_create(e_data.get("emergency_type").get("name"))[0]
    # severity = e_data.get("severity")
    #
    # brief_data = {"title": e_data.get("briefs")[0].get("title"),
    #               "text": e_data.get("briefs")[0].get("text"), "reporter": user}
    # brief = Brief.objects.create(**brief_data)
    #
    # filez = File.objects.bulk_create([file.file for file in files])
    # print(type(filez), "files_obj>>>>>>>>>>>>>")
    # brief.files.add(*filez)
    #
    # emergency = Emergency.objects.create(emergency_type=emergency_type, severity=severity)
    # emergency.respondents.add(user)
    # emergency.briefs.add(brief)
    # emergency.save()
    #
    # return emergency


@sync_to_async
def schema_to_dict(schema: ModelSchema) -> dict:
    return schema.dict()


@sync_to_async
def brief_data_from_e_dict_sync(emg_dict: dict, user: User) -> dict:
    return {
        "reporter": user,
        "title": emg_dict.get("briefs")[0].get("title"),
        "text": emg_dict.get("briefs")[0].get("text"),
    }


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
    d_file.save()
    return d_file


@sync_to_async
def get_responses_sync():
    return Emergency.filters.get_all_emergencies()

