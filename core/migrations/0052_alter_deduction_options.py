# Generated by Django 4.0.6 on 2023-05-07 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0051_alter_deduction_options_alter_saving_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deduction',
            options={'ordering': ['-transaction_date']},
        ),
    ]