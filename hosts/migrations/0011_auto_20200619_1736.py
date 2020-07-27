# Generated by Django 3.0.7 on 2020-06-19 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0010_host_host_template'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'verbose_name_plural': 'Itens'},
        ),
        migrations.AddField(
            model_name='item',
            name='item_intervaloAtualizacao',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='item',
            name='item_intervaloAtualizacaoUn',
            field=models.CharField(choices=[('sec', 'Segundos'), ('min', 'Minutos'), ('hrs', 'Horas'), ('dia', 'Dias'), ('mes', 'Meses'), ('ano', 'Anos')], default=('min', 'Minutos'), max_length=100),
        ),
        migrations.AddField(
            model_name='item',
            name='item_tempoArmazenamentoDados',
            field=models.PositiveSmallIntegerField(default=90),
        ),
        migrations.AddField(
            model_name='item',
            name='item_tempoArmazenamentoDadosUn',
            field=models.CharField(choices=[('sec', 'Segundos'), ('min', 'Minutos'), ('hrs', 'Horas'), ('dia', 'Dias'), ('mes', 'Meses'), ('ano', 'Anos')], default=('dia', 'Dias'), max_length=100),
        ),
        migrations.AddField(
            model_name='template',
            name='template_observacoes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
