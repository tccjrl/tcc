# Generated by Django 3.0.7 on 2020-06-30 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0013_auto_20200629_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='host_nomeTabela',
            field=models.DateTimeField(null=True),
        ),
    ]
