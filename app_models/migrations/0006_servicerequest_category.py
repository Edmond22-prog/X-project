# Generated by Django 5.1.6 on 2025-04-15 00:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_models', '0005_rename_serviceproposalcategory_servicecategory_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicerequest',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='requests', to='app_models.servicecategory'),
        ),
    ]
