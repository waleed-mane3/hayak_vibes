# Generated by Django 4.0.2 on 2022-06-25 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0002_design_created_at_design_update_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=1000)),
                ('last_name', models.CharField(max_length=1000)),
            ],
        ),
    ]
