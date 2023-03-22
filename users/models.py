import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.urls import reverse
from model_utils.models import TimeStampedModel


class CustomUser(AbstractUser):
    name = models.CharField(max_length=20, blank=True)

    class Meta:
        db_table = "auth_user"