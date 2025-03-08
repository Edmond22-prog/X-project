# Generated by Django 5.1.6 on 2025-03-08 04:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_models', '0003_userverification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicerequestsocials',
            name='service_request',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='app_models.servicerequest'),
        ),
        migrations.AlterField(
            model_name='usersocials',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='socials', to=settings.AUTH_USER_MODEL),
        ),
    ]
