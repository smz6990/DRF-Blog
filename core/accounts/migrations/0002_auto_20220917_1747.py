# Generated by Django 3.2.15 on 2022-09-17 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="image",
            field=models.ImageField(
                default="accounts/avatars/default.png",
                upload_to="accounts/avatars/",
            ),
        ),
    ]
