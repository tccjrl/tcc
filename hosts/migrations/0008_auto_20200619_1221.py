# Generated by Django 3.0.7 on 2020-06-19 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0007_itens_templates'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Itens',
            new_name='Item',
        ),
        migrations.RenameModel(
            old_name='Templates',
            new_name='Template',
        ),
    ]
