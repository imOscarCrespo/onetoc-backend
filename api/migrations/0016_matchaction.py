# Generated by Django 4.1.1 on 2023-01-08 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_match_tab'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.action')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.match')),
            ],
        ),
    ]