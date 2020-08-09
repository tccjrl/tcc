# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task

from funcoes_Tabelas.man_tabelas_itens import criaTabelaSnmpGet


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)

@shared_task
def hello_world():
    print('Hello World!')
    return 0

@shared_task
def cria_tabela_celery():
    criaTabelaSnmpGet('TASKCELERYTEST')
    return 0
