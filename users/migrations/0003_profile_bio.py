# Generated by Django 4.1.7 on 2023-03-26 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
    ]
