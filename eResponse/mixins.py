import uuid

from django.db import models


class TimeMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class IDMixin(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        db_index=True,
        default=uuid.uuid4,
        editable=False
    )

    class Meta:
        abstract = True

