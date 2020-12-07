# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task

from funcoes_snmp.snmp_get import snmpGet

from funcoes_Tabelas.create_tasks_helper import getItens, createTaskSnmpGet
from funcoes_Tabelas.man_tabelas_itens import insertSnmpGetResult

from django_celery_beat.models import IntervalSchedule, PeriodicTask


@shared_task
def task_snmp_get(host_nomeTabela_snmpGet, id_item, nome_item, ip, oid):
    info = snmpGet(ip, oid)
    insertSnmpGetResult(host_nomeTabela_snmpGet, id_item, nome_item, info)
    return info


@shared_task
def create_task_snmpGet_host_created(host_nomeTabela_snmpGet,
                                     host_ip,
                                     host_porta,
                                     host_status):
    itens = getItens(host_nomeTabela_snmpGet=host_nomeTabela_snmpGet,
                   host_ip=host_ip,
                   host_porta=host_porta,
                   host_status=host_status)

    for item in itens:
        createTaskSnmpGet(host_nomeTabela_snmpGet,
                          host_ip,
                          host_porta,
                          item.id,
                          item.item_nome,
                          item.item_oid,
                          item.item_intervaloAtualizacao,
                          item.item_intervaloAtualizacaoUn)
