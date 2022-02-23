# Generated by Django 3.2.10 on 2022-01-19 09:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transplants', '0003_transplant_donor_criteria'),
    ]

    operations = [
        migrations.AddField(
            model_name='transplant',
            name='donor_egfr',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(500.0)]),
        ),
    ]
