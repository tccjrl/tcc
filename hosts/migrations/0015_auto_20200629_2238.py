# Generated by Django 3.0.7 on 2020-06-30 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0014_auto_20200629_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='host_nomeTabela',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]