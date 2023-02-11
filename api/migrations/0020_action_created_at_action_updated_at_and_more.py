# Generated by Django 4.1.1 on 2023-01-14 09:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0019_remove_action_enabled_remove_event_disabled_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default='2021-09-27 15:22:53.679985+02'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='action',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, default='2021-09-27 15:22:53.679985+02'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='action',
            name='updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
