# Generated by Django 3.2.11 on 2022-01-24 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20220123_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='expires_in',
            field=models.DateTimeField(max_length=200),
        ),
    ]
