# Generated by Django 3.0.7 on 2020-06-30 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0012_host_host_nometabela'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='host_nomeTabela',
            field=models.DateTimeField(),
        ),
    ]
