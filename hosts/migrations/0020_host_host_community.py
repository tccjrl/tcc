# Generated by Django 3.1 on 2021-01-23 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0019_auto_20210117_2002'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='host_community',
            field=models.CharField(default='public', max_length=32),
        ),
    ]