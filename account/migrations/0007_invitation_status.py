# Generated by Django 4.0.2 on 2022-04-06 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_event_user_alter_invitation_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('wait', 'wait'), ('confirmed', 'confirmed'), ('apologize', 'apologize')], default='none', max_length=300),
        ),
    ]
