# Generated by Django 3.2.3 on 2021-06-22 15:52

from django.db import migrations, models
import pops.models


class Migration(migrations.Migration):

    dependencies = [
        ('pops', '0021_auto_20210224_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='casestudy',
            name='r_data',
            field=models.FileField(blank=True, help_text='R data file to run PoPS model', null=True, upload_to=pops.models.r_data_directory, verbose_name='R data file'),
        ),
    ]