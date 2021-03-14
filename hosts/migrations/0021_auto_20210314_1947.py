# Generated by Django 3.1 on 2021-03-14 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0020_host_host_community'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_tipoInformacao',
            field=models.CharField(choices=[('NI', 'Numérico(Inteiro)'), ('ND', 'Numérico(Decimal)'), ('CH', 'Caracter'), ('LG', 'Log')], max_length=100),
        ),
    ]
