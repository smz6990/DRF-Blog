# Generated by Django 3.2.15 on 2022-09-20 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20220917_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='accounts/avatars/default.jpg', null=True, upload_to='accounts/avatars/'),
        ),
    ]