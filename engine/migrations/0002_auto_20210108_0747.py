# Generated by Django 3.1.5 on 2021-01-08 07:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('engine', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
