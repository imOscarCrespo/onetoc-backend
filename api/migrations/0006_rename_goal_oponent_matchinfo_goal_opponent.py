# Generated by Django 4.1.1 on 2024-11-21 22:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_rename_red_card_oponent_matchinfo_corner_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='matchinfo',
            old_name='goal_oponent',
            new_name='goal_opponent',
        ),
    ]