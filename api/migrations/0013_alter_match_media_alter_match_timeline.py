# Generated by Django 4.1.1 on 2022-11-06 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_match_finished_at_match_started_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='media',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='timeline',
            field=models.URLField(null=True),
        ),
    ]
