# Generated by Django 3.1.6 on 2021-03-16 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factoryWebsite', '0007_auto_20210308_1604'),
    ]

    operations = [
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.SmallIntegerField()),
                ('y', models.SmallIntegerField()),
                ('color', models.CharField(choices=[('W', 'White'), ('R', 'Red'), ('B', 'Blue')], max_length=1)),
                ('status', models.CharField(choices=[('E', 'Empty'), ('EB', 'Emptybox'), ('F', 'Full')], default='F', max_length=2)),
            ],
        ),
    ]
