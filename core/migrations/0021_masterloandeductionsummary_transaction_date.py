# Generated by Django 4.0.6 on 2022-07-31 11:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_remove_masterloandeductionsummary_transaction_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='masterloandeductionsummary',
            name='transaction_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
