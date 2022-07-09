# Generated by Django 4.0.2 on 2022-04-18 23:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_alter_invitation_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='reference',
            field=models.CharField(default=uuid.uuid4, max_length=36),
        ),
    ]
