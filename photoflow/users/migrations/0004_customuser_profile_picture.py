# Generated by Django 3.2.16 on 2024-06-01 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_customuser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(default='default_img.jpg', upload_to='profile_pictures/'),
        ),
    ]