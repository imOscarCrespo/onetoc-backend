# Generated by Django 4.1.1 on 2024-11-20 22:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_club_status_tab_status_tabtype_status_team_status_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yellow_card', models.PositiveIntegerField(null=True)),
                ('yellow_card_oponent', models.PositiveIntegerField(null=True)),
                ('red_card', models.PositiveIntegerField(null=True)),
                ('red_card_oponent', models.PositiveIntegerField(null=True)),
                ('goal', models.PositiveIntegerField(null=True)),
                ('goal_oponent', models.PositiveIntegerField(null=True)),
                ('substitution', models.PositiveIntegerField(null=True)),
                ('substitution_oponent', models.PositiveIntegerField(null=True)),
                ('match', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.match')),
            ],
        ),
    ]