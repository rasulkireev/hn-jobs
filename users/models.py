import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from model_utils.models import TimeStampedModel


class CustomUser(AbstractUser):
    name = models.CharField(max_length=20, blank=True)

    class Meta:
        db_table = "auth_user"


class Subscriber(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField()
    confirmed = models.BooleanField(default=False)

    technology_selected = models.CharField(max_length=256)
