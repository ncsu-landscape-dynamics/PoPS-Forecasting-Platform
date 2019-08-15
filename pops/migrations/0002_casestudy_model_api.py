# Generated by Django 2.2.4 on 2019-08-15 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pops', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='casestudy',
            name='model_api',
            field=models.CharField(blank=True, help_text='Link to the model api for this case study.', max_length=250, verbose_name='model api url'),
        ),
    ]
