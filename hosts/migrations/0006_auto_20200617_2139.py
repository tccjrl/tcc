# Generated by Django 3.0.7 on 2020-06-18 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0005_auto_20200617_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='host_observacoes',
            field=models.TextField(blank=True, null=True),
        ),
    ]