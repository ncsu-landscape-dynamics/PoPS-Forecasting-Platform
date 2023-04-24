# Generated by Django 3.2.3 on 2021-05-21 12:26

import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pops', '0021_auto_20210224_1328'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlottingDistanceScale',
            fields=[
                ('parameters', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='pops.parameters', verbose_name='parameters')),
                ('values', django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=2, max_digits=7, validators=[django.core.validators.MinValueValidator(0)]), blank=True, help_text='Distance scale values', size=None, verbose_name='distance scale values')),
                ('probabilities', django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=3, max_digits=4, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)]), blank=True, help_text='Distance scale probabilities', size=None, verbose_name='distance scale probabilities')),
                ('minimum', models.DecimalField(blank=True, decimal_places=2, help_text='Minimum value in the array', max_digits=7, validators=[django.core.validators.MinValueValidator(0)], verbose_name='minimum')),
                ('maximum', models.DecimalField(blank=True, decimal_places=2, help_text='Maximum value in the array', max_digits=7, validators=[django.core.validators.MinValueValidator(0)], verbose_name='maximum')),
                ('most_probable_value', models.DecimalField(blank=True, decimal_places=2, help_text='Value in the array with the highest probability', max_digits=7, validators=[django.core.validators.MinValueValidator(0)], verbose_name='most probable value')),
                ('step_size', models.DecimalField(blank=True, decimal_places=2, help_text='Step size for the array', max_digits=5, validators=[django.core.validators.MinValueValidator(0)], verbose_name='step size')),
            ],
            options={
                'verbose_name': 'distance scale parameters for plotting',
                'verbose_name_plural': 'distance scale parameters for plotting',
            },
        ),
        migrations.CreateModel(
            name='PlottingReproductiveRate',
            fields=[
                ('parameters', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='pops.parameters', verbose_name='parameters')),
                ('values', django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=2, max_digits=7, validators=[django.core.validators.MinValueValidator(0)]), blank=True, help_text='Reproductive rate values', size=None, verbose_name='reproductive rate values')),
                ('probabilities', django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=3, max_digits=4, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)]), blank=True, help_text='Reproductive rate probabilities', size=None, verbose_name='reproductive rate probabilities')),
                ('minimum', models.DecimalField(blank=True, decimal_places=2, help_text='Minimum value in the array', max_digits=7, validators=[django.core.validators.MinValueValidator(0)], verbose_name='minimum')),
                ('maximum', models.DecimalField(blank=True, decimal_places=2, help_text='Maximum value in the array', max_digits=7, validators=[django.core.validators.MinValueValidator(0)], verbose_name='maximum')),
                ('most_probable_value', models.DecimalField(blank=True, decimal_places=2, help_text='Value in the array with the highest probability', max_digits=7, validators=[django.core.validators.MinValueValidator(0)], verbose_name='most probable value')),
                ('step_size', models.DecimalField(blank=True, decimal_places=2, help_text='Step size for the array', max_digits=5, validators=[django.core.validators.MinValueValidator(0)], verbose_name='step size')),
            ],
            options={
                'verbose_name': 'reproductive rate parameters for plotting',
                'verbose_name_plural': 'reproductive rate parameters for plotting',
            },
        ),
    ]