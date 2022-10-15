# Generated by Django 4.1.1 on 2022-10-14 14:54

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_action_default_action_enabled_action_events'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='events',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200, null=True), blank=True, default=list, size=None),
        ),
    ]