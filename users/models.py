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


class OutreachTemplate(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="outreach_template")
    title = models.CharField(max_length=256)
    subject_line = models.CharField(max_length=256)
    text = models.TextField(blank=True)
    cc_s = models.CharField(max_length=256)

    def __str__(self):
        return self.title


class Outreach(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="outreach")
    receiver = models.ForeignKey('profiles.profile', on_delete=models.CASCADE, related_name="outreach")
    subject_line = models.CharField(max_length=256)
    text = models.TextField(blank=True)
    cc_s = models.CharField(max_length=256)

    def get_absolute_url(self):
        return reverse("outreach", kwargs={"id": self.id})