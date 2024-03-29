# Generated by Django 4.0.6 on 2023-04-19 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0049_alter_profile_staff_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bank',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bank_account',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='marital_status',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='nok_phone',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='nok_relationship',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='staff_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
