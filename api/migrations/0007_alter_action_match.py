# Generated by Django 4.1.1 on 2023-04-15 08:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_action_auto_create'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='match',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.match'),
        ),
    ]