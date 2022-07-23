# Generated by Django 4.0.2 on 2022-07-10 01:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0015_event_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invitation',
            name='name',
        ),
        migrations.AddField(
            model_name='invitation',
            name='first_name',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='invitation',
            name='last_name',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
