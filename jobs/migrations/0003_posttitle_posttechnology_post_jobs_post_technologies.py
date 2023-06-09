# Generated by Django 4.1.7 on 2023-05-08 01:52

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0002_remove_post_metadata"),
    ]

    operations = [
        migrations.CreateModel(
            name="PostTitle",
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
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="jobs.post"
                    ),
                ),
                (
                    "title",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="jobs.title"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PostTechnology",
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
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="jobs.post"
                    ),
                ),
                (
                    "technology",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="jobs.technology",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="post",
            name="jobs",
            field=models.ManyToManyField(
                blank=True,
                related_name="post",
                through="jobs.PostTitle",
                to="jobs.title",
            ),
        ),
        migrations.AddField(
            model_name="post",
            name="technologies",
            field=models.ManyToManyField(
                blank=True,
                related_name="post",
                through="jobs.PostTechnology",
                to="jobs.technology",
            ),
        ),
    ]
