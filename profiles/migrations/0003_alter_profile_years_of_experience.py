# Generated by Django 4.1.1 on 2023-03-14 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0002_profile_years_of_experience"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="years_of_experience",
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
