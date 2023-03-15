import uuid
from autoslug import AutoSlugField
from django.db import models
from django.urls import reverse
from model_utils.models import TimeStampedModel

class Profile(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    latest_who_wants_to_be_hired_id = models.IntegerField()
    who_wants_to_be_hired_title = models.CharField(max_length=25)

    title = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    level = models.CharField(max_length=256, blank=True)
    willing_to_relocate = models.CharField(max_length=256, default="No")
    is_remote = models.BooleanField(default=False)
    technologies_used = models.ManyToManyField("Technology", related_name="profile", blank=True)
    years_of_experience = models.IntegerField(blank=True, null=True)
    capacity = models.CharField(max_length=100, blank=True)

    # GEO
    location = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)

    # Secret
    name = models.CharField(max_length=256, blank=True)
    resume_link = models.URLField(blank=True)
    personal_website = models.URLField(blank=True)
    email = models.EmailField(blank=True)
    who_wants_to_be_hired_comment_id = models.IntegerField()
    hn_username = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("profile", kwargs={"pk": self.id})

class Technology(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=256)
    slug = AutoSlugField(populate_from="name", always_update=True)

    def __str__(self):
        return self.name