# Generated by Django 3.2.15 on 2022-09-17 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_auto_20220917_1747"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
