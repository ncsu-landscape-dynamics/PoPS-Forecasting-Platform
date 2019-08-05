# Generated by Django 2.1.5 on 2019-05-24 17:55

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pops', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='created_by',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='created by'),
        ),
        migrations.AddField(
            model_name='run',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pops.Session', verbose_name='session id'),
        ),
        migrations.AddField(
            model_name='pest',
            name='case_study',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pops.CaseStudy', verbose_name='case study'),
        ),
        migrations.AddField(
            model_name='pest',
            name='pest_information',
            field=models.ForeignKey(blank=True, help_text='Sample help text.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='pops.PestInformation', verbose_name='pest'),
        ),
        migrations.AddField(
            model_name='output',
            name='run',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pops.Run', verbose_name='run id'),
        ),
        migrations.AddField(
            model_name='host',
            name='case_study',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pops.CaseStudy', verbose_name='case study'),
        ),
        migrations.AddField(
            model_name='creation',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pops.Host', verbose_name='host'),
        ),
        migrations.AddField(
            model_name='casestudy',
            name='calibration',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pops.CaseStudy', verbose_name='calibrated case study'),
        ),
        migrations.AddField(
            model_name='casestudy',
            name='created_by',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='created by'),
        ),
        migrations.CreateModel(
            name='LethalTemperature',
            fields=[
                ('weather', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='pops.Weather', verbose_name='weather')),
                ('lethal_type', models.CharField(choices=[('COLD', 'Cold'), ('HOT', 'Hot')], default='COLD', help_text='Is your pest killed by hot or cold temperatures?', max_length=4, verbose_name='lethal temperature type')),
                ('month', models.PositiveSmallIntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], default=1, help_text='What month does your lethal temperature occur?', verbose_name='month in which lethal temperature occurs')),
                ('value', models.DecimalField(blank=True, decimal_places=2, help_text='What is the lethal temperature at which pest/pathogen mortality occurs?', max_digits=4, validators=[django.core.validators.MinValueValidator(-50), django.core.validators.MaxValueValidator(50)], verbose_name='lethal temperature')),
                ('lethal_temperature_data', models.FileField(help_text='Upload your letah temperature data as a raster file (1 file with a layer for each year).', null=True, upload_to='documents', verbose_name='lethal temperature data')),
            ],
            options={
                'verbose_name': 'lethal temperature',
                'verbose_name_plural': 'lethal temperatures',
            },
        ),
        migrations.CreateModel(
            name='Precipitation',
            fields=[
                ('weather', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='pops.Weather', verbose_name='weather')),
                ('method', models.CharField(choices=[('RECLASS', 'Reclass'), ('POLYNOMIAL', 'Polynomial')], default='RECLASS', help_text='Choose a method to transform precipitation into a coefficient used by the model. Precipitation values are transformed into a value between 0 and 1.', max_length=30, verbose_name='precipitation coefficient creation method')),
                ('precipitation_data', models.FileField(help_text='Upload your precipitation data as a raster file (1 file with a layer for each timestep).', null=True, upload_to='documents', verbose_name='precipitation data')),
            ],
            options={
                'verbose_name': 'precipitation',
                'verbose_name_plural': 'precipitations',
            },
        ),
        migrations.CreateModel(
            name='Seasonality',
            fields=[
                ('weather', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='pops.Weather', verbose_name='weather')),
                ('first_month', models.PositiveSmallIntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], default=1, help_text='What is the first month your pest/pathogen spreads during the year?', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)], verbose_name='first month of season')),
                ('last_month', models.PositiveSmallIntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], default=12, help_text='What is the last month your pest/pathogen spreads during the year?', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)], verbose_name='last month of season')),
            ],
            options={
                'verbose_name': 'seasonality',
                'verbose_name_plural': 'seasonalities',
            },
        ),
        migrations.CreateModel(
            name='Temperature',
            fields=[
                ('weather', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='pops.Weather', verbose_name='weather')),
                ('method', models.CharField(choices=[('RECLASS', 'Reclass'), ('POLYNOMIAL', 'Polynomial')], default='RECLASS', help_text='Choose a method to transform temperature into a coefficient used by the model. Temperature values are transformed into a value between 0 and 1.', max_length=30, verbose_name='temperature coefficient creation method')),
                ('temperature_data', models.FileField(help_text='Upload your temperature data as a raster file (1 file with a layer for each timestep).', null=True, upload_to='documents', verbose_name='temperature data')),
            ],
            options={
                'verbose_name': 'temperature',
                'verbose_name_plural': 'temperatures',
            },
        ),
        migrations.CreateModel(
            name='Wind',
            fields=[
                ('weather', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='pops.Weather', verbose_name='weather')),
                ('wind_direction', models.CharField(choices=[('N', 'North'), ('NE', 'Northeast'), ('E', 'East'), ('SE', 'Southeast'), ('S', 'South'), ('SW', 'Southwest'), ('W', 'West'), ('NW', 'Northwest')], default='N', help_text='What is the predominate wind direction in your study area?', max_length=30, verbose_name='wind direction')),
                ('kappa', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12')], default=1, help_text='What is the average wind strength in your study area? 0 is no effect and 12 is very strong directional movement', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)], verbose_name='wind strenth (kappa)')),
            ],
            options={
                'verbose_name': 'wind',
                'verbose_name_plural': 'winds',
            },
        ),
        migrations.CreateModel(
            name='PrecipitationPolynomial',
            fields=[
                ('precipitation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='pops.Precipitation', verbose_name='precipitation')),
                ('degree', models.PositiveSmallIntegerField(choices=[(1, 'One'), (2, 'Two'), (3, 'Three')], default=1, help_text='Select the degree of your polynomial function.', verbose_name='polynomial degree')),
                ('a0', models.DecimalField(blank=True, decimal_places=5, help_text='value of a0 in your polynomial transformation.', max_digits=8, null=True, verbose_name='a0')),
                ('a1', models.DecimalField(blank=True, decimal_places=5, help_text='value of a1 in your polynomial transformation.', max_digits=8, null=True, verbose_name='a1')),
                ('a2', models.DecimalField(blank=True, decimal_places=5, help_text='value of a2 in your polynomial transformation.', max_digits=8, null=True, verbose_name='a2')),
                ('a3', models.DecimalField(blank=True, decimal_places=5, help_text='value of a3 in your polynomial transformation.', max_digits=8, null=True, verbose_name='a3')),
                ('x1', models.DecimalField(blank=True, decimal_places=2, help_text='value of x1 in your polynomial transformation.', max_digits=5, null=True, verbose_name='x1')),
                ('x2', models.DecimalField(blank=True, decimal_places=2, help_text='value of x2 in your polynomial transformation.', max_digits=5, null=True, verbose_name='x2')),
                ('x3', models.DecimalField(blank=True, decimal_places=2, help_text='value of x3 in your polynomial transformation.', max_digits=5, null=True, verbose_name='x3')),
            ],
            options={
                'verbose_name': 'precipitation polynomial',
                'verbose_name_plural': 'precipitation polynomials',
            },
        ),
        migrations.CreateModel(
            name='TemperaturePolynomial',
            fields=[
                ('temperature', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='pops.Temperature', verbose_name='temperature')),
                ('degree', models.PositiveSmallIntegerField(choices=[(1, 'One'), (2, 'Two'), (3, 'Three')], default=1, help_text='Select the degree of your polynomial function.', verbose_name='polynomial degree')),
                ('a0', models.DecimalField(blank=True, decimal_places=5, help_text='value of a0 in your polynomial transformation.', max_digits=8, null=True, verbose_name='a0')),
                ('a1', models.DecimalField(blank=True, decimal_places=5, help_text='value of a1 in your polynomial transformation.', max_digits=8, null=True, verbose_name='a1')),
                ('a2', models.DecimalField(blank=True, decimal_places=5, help_text='value of a2 in your polynomial transformation.', max_digits=8, null=True, verbose_name='a2')),
                ('a3', models.DecimalField(blank=True, decimal_places=5, help_text='value of a3 in your polynomial transformation.', max_digits=8, null=True, verbose_name='a3')),
                ('x1', models.DecimalField(blank=True, decimal_places=2, help_text='value of x1 in your polynomial transformation.', max_digits=5, null=True, verbose_name='x1')),
                ('x2', models.DecimalField(blank=True, decimal_places=2, help_text='value of x2 in your polynomial transformation.', max_digits=5, null=True, verbose_name='x2')),
                ('x3', models.DecimalField(blank=True, decimal_places=2, help_text='value of x3 in your polynomial transformation.', max_digits=5, null=True, verbose_name='x3')),
            ],
            options={
                'verbose_name': 'temperature polynomial',
                'verbose_name_plural': 'temperature polynomials',
            },
        ),
        migrations.AddField(
            model_name='temperaturereclass',
            name='temperature',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pops.Temperature', verbose_name='temperature'),
        ),
        migrations.AddField(
            model_name='precipitationreclass',
            name='precipitation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pops.Precipitation', verbose_name='precipitation'),
        ),
    ]