# Generated by Django 5.0.2 on 2025-04-04 22:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apphub', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='user_images/'),
        ),
    ]
