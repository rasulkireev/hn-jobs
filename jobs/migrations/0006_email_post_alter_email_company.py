# Generated by Django 4.1.7 on 2023-05-12 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("jobs", "0005_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="email",
            name="post",
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.CASCADE, related_name="email", to="jobs.post"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="email",
            name="company",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="email", to="jobs.company"
            ),
        ),
    ]
