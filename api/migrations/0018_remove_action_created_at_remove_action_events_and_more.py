# Generated by Django 4.1.1 on 2023-01-14 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_event_tab_team_delete_matchaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='action',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='action',
            name='events',
        ),
        migrations.RemoveField(
            model_name='action',
            name='updated_at',
        ),
    ]