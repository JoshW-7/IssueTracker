# Generated by Django 3.2.1 on 2021-05-06 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0006_auto_20210505_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
