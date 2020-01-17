# Generated by Django 3.0 on 2020-01-15 23:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='What is the department name (e.g. NCSU, APHIS)?', max_length=150, verbose_name='department')),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='What is the organization name (e.g. NCSU, APHIS)?', max_length=150, verbose_name='team member organization')),
            ],
        ),
        migrations.RemoveField(
            model_name='member',
            name='name',
        ),
        migrations.AddField(
            model_name='member',
            name='first_name',
            field=models.CharField(help_text="What is the team member's name?", max_length=150, null=True, verbose_name='first name'),
        ),
        migrations.AddField(
            model_name='member',
            name='github',
            field=models.URLField(blank=True, help_text="What is member's GitHub URL?", null=True, verbose_name='team member github URL'),
        ),
        migrations.AddField(
            model_name='member',
            name='last_name',
            field=models.CharField(help_text="What is the team member's name?", max_length=150, null=True, verbose_name='last name'),
        ),
        migrations.AddField(
            model_name='member',
            name='title',
            field=models.CharField(help_text="What is the team member's title?", max_length=100, null=True, verbose_name='team member title'),
        ),
        migrations.AlterField(
            model_name='member',
            name='category',
            field=models.CharField(choices=[('CURRENT', 'Current Member'), ('PAST', 'Past Member'), ('AFFILIATE', 'Affiliate')], default='CURRENT', help_text="What is the member's category?", max_length=20, null=True, verbose_name='member type'),
        ),
        migrations.AlterField(
            model_name='member',
            name='picture',
            field=models.FileField(help_text='Upload team member image.', null=True, upload_to='team_images', verbose_name="team member's picture"),
        ),
        migrations.AlterField(
            model_name='member',
            name='role',
            field=models.CharField(help_text="What is the team member's role in the project?", max_length=200, null=True, verbose_name='team member role'),
        ),
        migrations.AddField(
            model_name='member',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='team.Department', verbose_name='organization'),
        ),
        migrations.AddField(
            model_name='member',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='team.Organization', verbose_name='organization'),
        ),
    ]
