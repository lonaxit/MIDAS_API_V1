# Generated by Django 4.0.6 on 2022-10-22 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_alter_deduction_options_masterloandeduction_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saving',
            name='credit',
            field=models.DecimalField(blank=True, decimal_places=2, default='0.00', max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='saving',
            name='debit',
            field=models.DecimalField(blank=True, decimal_places=2, default='0.00', max_digits=20, null=True),
        ),
    ]
