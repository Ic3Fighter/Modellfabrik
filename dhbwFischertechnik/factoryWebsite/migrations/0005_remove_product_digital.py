# Generated by Django 3.1.6 on 2021-03-07 14:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('factoryWebsite', '0004_auto_20210306_2214'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='digital',
        ),
    ]
