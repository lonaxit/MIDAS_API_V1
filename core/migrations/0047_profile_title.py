# Generated by Django 4.0.6 on 2023-04-19 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0046_deduction_deduction_sub_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='title',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
