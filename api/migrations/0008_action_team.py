# Generated by Django 4.1.1 on 2023-04-16 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_action_match'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.team'),
        ),
    ]
