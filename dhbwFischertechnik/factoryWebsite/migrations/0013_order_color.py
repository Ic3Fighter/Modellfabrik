# Generated by Django 3.1.6 on 2021-03-29 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factoryWebsite', '0012_auto_20210329_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='color',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
