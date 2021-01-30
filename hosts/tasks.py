# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task

from funcoes_snmp.snmp_get import snmpGet

from funcoes_Tabelas.create_tasks_helper import getItens, createTaskSnmpGet, createTaskCleanData
from funcoes_Tabelas.man_tabelas_itens import insertSnmpGetResult, clean_data

from django_celery_beat.models import PeriodicTask, IntervalSchedule

from .models import Host, Item, Template

import time


@shared_task
def task_snmp_get(host_nomeTabela_snmpGet, host_community, id_item, nome_item, ip, oid, porta, template_ids):
    info = snmpGet(ip=ip, oid=oid, porta=porta, community=host_community)
    insertSnmpGetResult(host_nomeTabela_snmpGet, id_item, nome_item, info)
    return info


@shared_task
def create_task_snmpGet_host_created(host_nomeTabela_snmpGet,
                                     host_ip,
                                     host_porta,
                                     host_status,
                                     host_community):
    itens = getItens(host_nomeTabela_snmpGet=host_nomeTabela_snmpGet,
                     host_ip=host_ip,
                     host_porta=host_porta,
                     host_status=host_status)

    for item in itens:
        templates = Template.objects.filter(template_item__id=item.id,
                                            host__host_nomeTabela_snmpGet=host_nomeTabela_snmpGet,
                                            host__host_ip=host_ip,
                                            host__host_porta=host_porta,
                                            host__host_status=host_status)

        createTaskSnmpGet(host_nomeTabela_snmpGet=host_nomeTabela_snmpGet,
                          host_ip=host_ip,
                          host_porta=host_porta,
                          host_community=host_community,
                          templates=templates,
                          item_id=item.id,
                          item_nome=item.item_nome,
                          item_oid=item.item_oid,
                          item_intervaloAtualizacao=item.item_intervaloAtualizacao,
                          item_intervaloAtualizacaoUn=item.item_intervaloAtualizacaoUn,)


@shared_task
def create_task_snmpGet_host_updated(host_nomeTabela_snmpGet,
                                     host_ip,
                                     host_porta,
                                     host_status,
                                     host_community):
    lista_PeriodicTasks_cadastradas = PeriodicTask.objects.filter(name__contains=('SNMPGETTASK=' + host_nomeTabela_snmpGet))

    for periodicTask in lista_PeriodicTasks_cadastradas:
        try:
            periodicTask.delete()
        except Exception as e:
            print(str(e.args[0]))
            time.sleep(4)
            periodicTask.delete()

    if host_status:
        itens = getItens(host_nomeTabela_snmpGet=host_nomeTabela_snmpGet,
                         host_ip=host_ip,
                         host_porta=host_porta,
                         host_status=host_status)

        for item in itens:
            templates = Template.objects.filter(template_item__id=item.id,
                                                host__host_nomeTabela_snmpGet=host_nomeTabela_snmpGet,
                                                host__host_ip=host_ip,
                                                host__host_porta=host_porta,
                                                host__host_status=host_status)

            createTaskSnmpGet(host_nomeTabela_snmpGet=host_nomeTabela_snmpGet,
                              host_ip=host_ip,
                              host_porta=host_porta,
                              host_community=host_community,
                              templates=templates,
                              item_id=item.id,
                              item_nome=item.item_nome,
                              item_oid=item.item_oid,
                              item_intervaloAtualizacao=item.item_intervaloAtualizacao,
                              item_intervaloAtualizacaoUn=item.item_intervaloAtualizacaoUn)


@shared_task
def create_task_snmpGet_template_updated(template_id, template_nome):
    hosts = Host.objects.filter(host_template__template_nome=template_nome,
                                host_template__id=template_id)

    for host in hosts:
        lista_PeriodicTasks_cadastradas = PeriodicTask.objects.filter(name__contains=('SNMPGETTASK=' + host.host_nomeTabela_snmpGet))

        for periodicTask in lista_PeriodicTasks_cadastradas:
            periodicTask.delete()

        if host.host_status:
            itens = getItens(host_nomeTabela_snmpGet=host.host_nomeTabela_snmpGet,
                             host_ip=host.host_ip,
                             host_porta=host.host_porta,
                             host_status=host.host_status)

            for item in itens:
                templates = Template.objects.filter(template_item__id=item.id,
                                                    host__host_nomeTabela_snmpGet=host.host_nomeTabela_snmpGet,
                                                    host__host_ip=host.host_ip,
                                                    host__host_porta=host.host_porta,
                                                    host__host_status=host.host_status)

                createTaskSnmpGet(host_nomeTabela_snmpGet=host.host_nomeTabela_snmpGet,
                                  host_ip=host.host_ip,
                                  host_porta=host.host_porta,
                                  host_community=host.host_community,
                                  templates=templates,
                                  item_id=item.id,
                                  item_nome=item.item_nome,
                                  item_oid=item.item_oid,
                                  item_intervaloAtualizacao=item.item_intervaloAtualizacao,
                                  item_intervaloAtualizacaoUn=item.item_intervaloAtualizacaoUn)


@shared_task
def create_task_snmpGet_template_deleted(hosts_ids):
    for host_id in hosts_ids:
        hosts = Host.objects.filter(id=host_id)

    for host in hosts:
        lista_PeriodicTasks_cadastradas = PeriodicTask.objects.filter(name__contains=('SNMPGETTASK=' + host.host_nomeTabela_snmpGet))
        print(lista_PeriodicTasks_cadastradas)

        for periodicTask in lista_PeriodicTasks_cadastradas:
            periodicTask.delete()

        if host.host_status:
            itens = getItens(host_nomeTabela_snmpGet=host.host_nomeTabela_snmpGet,
                             host_ip=host.host_ip,
                             host_porta=host.host_porta,
                             host_status=host.host_status)

            for item in itens:
                templates = Template.objects.filter(template_item__id=item.id,
                                                    host__host_nomeTabela_snmpGet=host.host_nomeTabela_snmpGet,
                                                    host__host_ip=host.host_ip,
                                                    host__host_porta=host.host_porta,
                                                    host__host_status=host.host_status)

                createTaskSnmpGet(host_nomeTabela_snmpGet=host.host_nomeTabela_snmpGet,
                                  host_ip=host.host_ip,
                                  host_porta=host.host_porta,
                                  host_community=host.host_community,
                                  templates=templates,
                                  item_id=item.id,
                                  item_nome=item.item_nome,
                                  item_oid=item.item_oid,
                                  item_intervaloAtualizacao=item.item_intervaloAtualizacao,
                                  item_intervaloAtualizacaoUn=item.item_intervaloAtualizacaoUn)


@shared_task
def create_task_snmpGet_item_updated(item_id,
                                     item_nome_old,
                                     item_oid_old,
                                     item_intervaloAtualizacao_old,
                                     item_intervaloAtualizacaoUn_old):
    lista_periodicTasks = PeriodicTask.objects.filter(name__contains=('_item_id:' + str(item_id))).filter(name__contains=('SNMPGETTASK'))
    item = Item.objects.get(id=item_id)

    for periodicTask in lista_periodicTasks:
        args = periodicTask.args
        print(item_nome_old, item_oid_old)
        args = args.replace('"' + item_nome_old + '"', '"' + item.item_nome + '"')
        args = args.replace('"' + item_oid_old + '"', '"' + item.item_oid + '"')
        periodicTask.args = args

        intervalo_id = None

        novoIntervalo = IntervalSchedule(every=item_intervaloAtualizacao_old,
                                         period=item_intervaloAtualizacaoUn_old)

        intervalosCadastrados = IntervalSchedule.objects.all()

        for intervalo in intervalosCadastrados:
            if (intervalo.every == novoIntervalo.every) and (intervalo.period == novoIntervalo.period):
                intervalo_id = intervalo.id
                print('ACHEI UM INTERVALO NO BD')

        if intervalo_id is None:
            novoIntervalo.save()
            intervalo_id = novoIntervalo.id
            print('NÃO ACHEI UM INTERVALO E SALVEI NO BD')

        periodicTask.interval_id = intervalo_id

        periodicTask.save()


# =======================================================================================================================
@shared_task
def task_clean_data(item_id,
                    item_tempoArmazenamentoDados,
                    item_tempoArmazenamentoDadosUn,
                    host_nomeTabela_snmpGet):
    clean_data(item_id=item_id,
               item_tempoArmazenamentoDados=item_tempoArmazenamentoDados,
               item_tempoArmazenamentoDadosUn=item_tempoArmazenamentoDadosUn,
               host_nomeTabela_snmpGet=host_nomeTabela_snmpGet)

@shared_task
def create_task_CleanData_host_created(host_nomeTabela_snmpGet,
                                     host_ip,
                                     host_porta,
                                     host_status):
    itens = getItens(host_nomeTabela_snmpGet=host_nomeTabela_snmpGet,
                     host_ip=host_ip,
                     host_porta=host_porta,
                     host_status=host_status)

    for item in itens:
        templates = Template.objects.filter(template_item__id=item.id,
                                            host__host_nomeTabela_snmpGet=host_nomeTabela_snmpGet,
                                            host__host_ip=host_ip,
                                            host__host_porta=host_porta,
                                            host__host_status=host_status)

        createTaskCleanData(host_nomeTabela_snmpGet=host_nomeTabela_snmpGet,
                            templates=templates,
                            item_id=item.id,
                            item_tempoArmazenamentoDados=item.item_tempoArmazenamentoDados,
                            item_tempoArmazenamentoDadosUn=item.item_tempoArmazenamentoDadosUn)

@shared_task
def create_task_CleanData_host_updated(host_nomeTabela_snmpGet,
                                     host_ip,
                                     host_porta,
                                     host_status):
    lista_PeriodicTasks_cadastradas = PeriodicTask.objects.filter(name__contains=('CLEANDATATASK=' + host_nomeTabela_snmpGet))

    for periodicTask in lista_PeriodicTasks_cadastradas:
        try:
            periodicTask.delete()
        except Exception as e:
            print(str(e.args[0]))
            time.sleep(4)
            periodicTask.delete()

    if host_status:
        itens = getItens(host_nomeTabela_snmpGet=host_nomeTabela_snmpGet,
                         host_ip=host_ip,
                         host_porta=host_porta,
                         host_status=host_status)

        for item in itens:
            templates = Template.objects.filter(template_item__id=item.id,
                                                host__host_nomeTabela_snmpGet=host_nomeTabela_snmpGet,
                                                host__host_ip=host_ip,
                                                host__host_porta=host_porta,
                                                host__host_status=host_status)

            createTaskCleanData(host_nomeTabela_snmpGet=host_nomeTabela_snmpGet,
                                templates=templates,
                                item_id=item.id,
                                item_tempoArmazenamentoDados=item.item_tempoArmazenamentoDados,
                                item_tempoArmazenamentoDadosUn=item.item_tempoArmazenamentoDadosUn)

@shared_task
def create_task_CleanData_template_updated(template_id, template_nome):
    hosts = Host.objects.filter(host_template__template_nome=template_nome,
                                host_template__id=template_id)

    for host in hosts:
        lista_PeriodicTasks_cadastradas = PeriodicTask.objects.filter(name__contains=('CLEANDATATASK=' + host.host_nomeTabela_snmpGet))

        for periodicTask in lista_PeriodicTasks_cadastradas:
            periodicTask.delete()

        if host.host_status:
            itens = getItens(host_nomeTabela_snmpGet=host.host_nomeTabela_snmpGet,
                             host_ip=host.host_ip,
                             host_porta=host.host_porta,
                             host_status=host.host_status)

            for item in itens:
                templates = Template.objects.filter(template_item__id=item.id,
                                                    host__host_nomeTabela_snmpGet=host.host_nomeTabela_snmpGet,
                                                    host__host_ip=host.host_ip,
                                                    host__host_porta=host.host_porta,
                                                    host__host_status=host.host_status)

                createTaskCleanData(host_nomeTabela_snmpGet=host.host_nomeTabela_snmpGet,
                                    templates=templates,
                                    item_id=item.id,
                                    item_tempoArmazenamentoDados=item.item_tempoArmazenamentoDados,
                                    item_tempoArmazenamentoDadosUn=item.item_tempoArmazenamentoDadosUn)


@shared_task
def create_task_CleanData_template_deleted(hosts_ids):
    for host_id in hosts_ids:
        hosts = Host.objects.filter(id=host_id)

    for host in hosts:
        lista_PeriodicTasks_cadastradas = PeriodicTask.objects.filter(name__contains=('CLEANDATATASK=' + host.host_nomeTabela_snmpGet))
        print(lista_PeriodicTasks_cadastradas)

        for periodicTask in lista_PeriodicTasks_cadastradas:
            periodicTask.delete()

        if host.host_status:
            itens = getItens(host_nomeTabela_snmpGet=host.host_nomeTabela_snmpGet,
                             host_ip=host.host_ip,
                             host_porta=host.host_porta,
                             host_status=host.host_status)

            for item in itens:
                templates = Template.objects.filter(template_item__id=item.id,
                                                    host__host_nomeTabela_snmpGet=host.host_nomeTabela_snmpGet,
                                                    host__host_ip=host.host_ip,
                                                    host__host_porta=host.host_porta,
                                                    host__host_status=host.host_status)

                createTaskCleanData(host_nomeTabela_snmpGet=host.host_nomeTabela_snmpGet,
                                    templates=templates,
                                    item_id=item.id,
                                    item_tempoArmazenamentoDados=item.item_tempoArmazenamentoDados,
                                    item_tempoArmazenamentoDadosUn=item.item_tempoArmazenamentoDadosUn)


@shared_task
def create_task_CleanData_item_updated(item_id,
                                     item_tempoArmazenamentoDados_old,
                                     item_tempoArmazenamentoDadosUn_old):
    lista_periodicTasks = PeriodicTask.objects.filter(name__contains=('_item_id:' + str(item_id))).filter(name__contains=('CLEANDATATASK'))
    item = Item.objects.get(id=item_id)

    for periodicTask in lista_periodicTasks:
        args = periodicTask.args
        args = args.replace('"' + str(item_tempoArmazenamentoDados_old) + '"', ('"' + str(item.item_tempoArmazenamentoDados) + '"'))
        args = args.replace('"' + item_tempoArmazenamentoDadosUn_old + '"', '"' + item.item_tempoArmazenamentoDadosUn + '"')
        periodicTask.args = args

        intervalo_id = None

        novoIntervalo = IntervalSchedule(every=1,
                                         period='minutes')

        intervalosCadastrados = IntervalSchedule.objects.all()

        for intervalo in intervalosCadastrados:
            if (intervalo.every == novoIntervalo.every) and (intervalo.period == novoIntervalo.period):
                intervalo_id = intervalo.id
                print('ACHEI UM INTERVALO NO BD')

        if intervalo_id is None:
            novoIntervalo.save()
            intervalo_id = novoIntervalo.id
            print('NÃO ACHEI UM INTERVALO E SALVEI NO BD')

        periodicTask.interval_id = intervalo_id

        periodicTask.save()