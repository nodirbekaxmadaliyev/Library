# Generated by Django 5.1.6 on 2025-03-11 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_book_book_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
