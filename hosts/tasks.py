# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task

from funcoes_Tabelas.man_tabelas_itens import criaTabelaSnmpGet


@shared_task
def add(x, y):
    return x + y

@shared_task
def hello_world():
    print('Hello World!')
    return 0
