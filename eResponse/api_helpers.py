from asgiref.sync import sync_to_async
from typing import Union, List
from djantic.main import ModelSchema
from django.db import models
from django.db.models import QuerySet


@sync_to_async
def to_schema(django_obj: Union[type(models), type(QuerySet), List], schema: ModelSchema):
    # print(django_obj, type(django_obj), ">>>>>>...,,,,,,,kklll;;", type(django_obj[0]))

    if hasattr(django_obj, "append") and isinstance(django_obj, list):
        return schema.from_django(django_obj, many=True)
    elif hasattr(django_obj, "count") and isinstance(django_obj, QuerySet):
        if django_obj.count() == 1:
            return schema.from_django(django_obj)
        return schema.from_django(django_obj, many=True)
    elif isinstance(django_obj, type(models)):
        return schema.from_orm(django_obj)


    # print(django_obj, type(django_obj), "<<<<.>>>......////////")
    # # print(django_obj.briefs.last().files.all())
    # if hasattr(django_obj, "count"):
    #     if django_obj.count() > 1:
    #         return schema.from_django(django_obj, many=True)
    #     return schema.from_orm(django_obj.get())
    # return schema.from_orm(django_obj)

    # if hasattr(django_obj, "count"):  # queryset.count
    #     return schema.from_django(django_obj, many=True)
    # return schema.from_orm(django_obj)
