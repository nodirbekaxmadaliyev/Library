# Generated by Django 5.1.6 on 2025-03-09 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_customuser_email_customuser_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='email',
            field=models.EmailField(default='nodirbekaxmadaliyev4888@gmail.com', max_length=254, unique=True),
            preserve_default=False,
        ),
    ]
