# Generated by Django 3.1.5 on 2021-01-17 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0007_stock_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='shares',
            field=models.FloatField(),
        ),
    ]
