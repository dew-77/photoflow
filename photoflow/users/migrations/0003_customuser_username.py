# Generated by Django 3.2.16 on 2024-06-01 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='username',
            field=models.CharField(default=1, max_length=30, unique=True),
            preserve_default=False,
        ),
    ]