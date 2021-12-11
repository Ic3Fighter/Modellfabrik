# Generated by Django 3.1.6 on 2021-03-26 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factoryWebsite', '0008_storage'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Storage',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='email',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='user',
        ),
        migrations.AddField(
            model_name='customer',
            name='timestamp',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
