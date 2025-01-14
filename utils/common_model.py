from django.db import models
from uuid import uuid4


class CommonModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False,
    )

    created_at = models.DateTimeField(
        "Created at",
        auto_now_add=True,
    )
    modified_at = models.DateTimeField(
        "Modified at",
        auto_now=True,
    )

    class Meta:
        abstract = True
