# Generated by Django 3.1.6 on 2021-03-08 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factoryWebsite', '0006_delete_shippingaddress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]
