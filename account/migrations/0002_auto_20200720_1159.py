# Generated by Django 3.0.8 on 2020-07-20 18:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=15, unique=True, validators=[django.core.validators.RegexValidator(message="phone number mustbe entered in the format:'+99999999'. up tho 14 digits allowed.", regex='^\\+?0?\\d{9,14}s')]),
        ),
    ]