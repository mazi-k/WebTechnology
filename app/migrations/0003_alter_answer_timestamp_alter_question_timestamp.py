# Generated by Django 4.2.6 on 2023-11-13 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
