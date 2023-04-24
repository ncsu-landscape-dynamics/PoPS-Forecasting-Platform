# Generated by Django 3.2.5 on 2022-01-16 19:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pops', '0026_alter_pesticide_default_application_month'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pesticide',
            name='default_application_month',
            field=models.IntegerField(blank=True, default=4, help_text='Default month for pesticide application (1-12)', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)], verbose_name='default month of pesticide application'),
        ),
    ]