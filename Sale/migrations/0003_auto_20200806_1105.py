# Generated by Django 3.0.8 on 2020-08-06 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Sale', '0002_productcart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcart',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Sale.Cart'),
        ),
    ]