from asgiref.sync import sync_to_async
from typing import Union
from djantic.main import ModelSchema
from django.db import models
from django.db.models import QuerySet


@sync_to_async
def to_schema(django_obj: Union[type(models), type(QuerySet)], schema: ModelSchema):
    if hasattr(django_obj, "count"):  # queryset.count
        return schema.from_django(django_obj, many=True)
    return schema.from_orm(django_obj)
