# Generated by Django 4.1.1 on 2023-03-14 04:49

import autoslug.fields
from django.db import migrations, models
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Technology",
            fields=[
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=256)),
                (
                    "slug",
                    autoslug.fields.AutoSlugField(
                        always_update=True, editable=False, populate_from="name"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="created",
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now,
                        editable=False,
                        verbose_name="modified",
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("latest_who_wants_to_be_hired_id", models.IntegerField()),
                ("who_wants_to_be_hired_titles", models.TextField()),
                ("who_wants_to_be_hired_comment_id", models.IntegerField()),
                ("title", models.CharField(max_length=256)),
                ("name", models.CharField(blank=True, max_length=256)),
                ("description", models.TextField(blank=True)),
                ("location", models.CharField(blank=True, max_length=100)),
                ("level", models.CharField(blank=True, max_length=256)),
                ("is_remote", models.BooleanField(default=False)),
                ("willing_to_relocate", models.BooleanField(default=False)),
                ("resume_link", models.URLField(blank=True)),
                ("personal_website", models.URLField(blank=True)),
                ("email", models.EmailField(blank=True, max_length=254)),
                (
                    "technologies_used",
                    models.ManyToManyField(
                        blank=True, related_name="profile", to="profiles.technology"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
