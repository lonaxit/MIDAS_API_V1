# Generated by Django 4.0.6 on 2022-10-28 14:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_customuser_gender_customuser_home_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='avatar',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='bank',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='bank_account',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='dob',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='email',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='employment_type',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='home_address',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='ippis_number',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='job_cadre',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='marital_status',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='nok_fullName',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='nok_phone',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='nok_relationship',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='phone',
        ),
    ]
