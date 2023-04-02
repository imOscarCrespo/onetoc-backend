# Generated by Django 4.1.1 on 2023-02-26 19:45

import api.websocket
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import enumfields.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0003_alter_action_events_event'),
    ]

    operations = [
        migrations.CreateModel(
            name='Websocket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=30, unique=True)),
                ('connection', models.CharField(max_length=30)),
                ('status', enumfields.fields.EnumField(default='OPENED', enum=api.websocket.Websocket_status, max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('match', models.ForeignKey(null=True,on_delete=django.db.models.deletion.CASCADE, to='api.match')),
                ('updated_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]