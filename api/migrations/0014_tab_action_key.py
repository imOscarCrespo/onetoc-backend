# Generated by Django 4.1.1 on 2022-12-25 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_alter_match_media_alter_match_timeline'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tab',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('icon', models.CharField(max_length=30)),
                ('order', models.PositiveBigIntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='action',
            name='key',
            field=models.CharField(max_length=30, null=True),
        ),
    ]