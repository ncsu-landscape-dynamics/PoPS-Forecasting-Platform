# Generated by Django 3.1.4 on 2021-01-12 23:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pops', '0007_auto_20210112_0900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicdata',
            name='year',
            field=models.PositiveIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MinValueValidator(2000)], verbose_name='historic data year'),
        ),
    ]