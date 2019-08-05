# Generated by Django 2.2.2 on 2019-06-18 16:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pops', '0010_auto_20190618_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='output',
            name='infected_area',
            field=models.DecimalField(blank=True, decimal_places=2, default=1, help_text='Overall infected area from the run.', max_digits=16, validators=[django.core.validators.MinValueValidator(0)], verbose_name='infected_area (m^2)'),
        ),
        migrations.AlterField(
            model_name='run',
            name='management_area',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=16, null=True, verbose_name='management area'),
        ),
    ]