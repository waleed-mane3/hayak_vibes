# Generated by Django 4.0.2 on 2022-05-21 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_alter_invitation_reference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('waiting', 'waiting'), ('confirmed', 'confirmed'), ('apologized', 'apologized'), ('checked', 'checked')], default='pending', max_length=300),
        ),
    ]
