from hosts.models import Item, Template
from django_celery_beat.models import IntervalSchedule, PeriodicTask


def getItens(host_nomeTabela_snmpGet,
             host_ip,
             host_porta,
             host_status):
    itens = Item.objects.filter(template__host__host_nomeTabela_snmpGet=host_nomeTabela_snmpGet,
                                template__host__host_ip=host_ip,
                                template__host__host_porta=host_porta,
                                template__host__host_status=host_status)

    itens_nao_repetidos = []
    for item in itens:
        if item not in itens_nao_repetidos:
            itens_nao_repetidos.append(item)

    return itens_nao_repetidos


def createTaskSnmpGet(host_nomeTabela_snmpGet,
                      host_ip,
                      host_porta,
                      host_community,
                      templates,
                      item_id,
                      item_nome,
                      item_oid,
                      item_intervaloAtualizacao,
                      item_intervaloAtualizacaoUn):
    template_ids = ''
    for template in templates:
        template_ids = template_ids + ('_template_id:' + str(template.id))

    intervalo_id = None

    novoIntervalo = IntervalSchedule(every=item_intervaloAtualizacao, period=item_intervaloAtualizacaoUn)

    intervalosCadastrados = IntervalSchedule.objects.all()

    for intervalo in intervalosCadastrados:
        if (intervalo.every == novoIntervalo.every) and (intervalo.period == novoIntervalo.period):
            intervalo_id = intervalo.id
            print('ACHEI UM INTERVALO NO BD')

    if intervalo_id is None:
        novoIntervalo.save()
        intervalo_id = novoIntervalo.id
        print('NÃO ACHEI UM INTERVALO E SALVEI NO BD')

    novaTask = PeriodicTask(
        name='SNMPGETTASK=' + host_nomeTabela_snmpGet + str(template_ids) + '_item_id:' + str(item_id),
        task='hosts.tasks.task_snmp_get',
        args='[' + '"' + host_nomeTabela_snmpGet + '", "' + host_community + '", "' + str(
            item_id) + '", "' + item_nome + '", "' + host_ip + '", "' + item_oid + '", "' + str(
            host_porta) + '", "' + str(template_ids) + '"]',
        kwargs='{}',
        enabled=1,
        interval_id=intervalo_id,
        one_off=0,
        headers='{}')
    novaTask.save()
    print('CRIEI UMA NOVA TAREFA')


# =======================================================================================================================
def createTaskCleanData(host_nomeTabela_snmpGet,
                        templates,
                        item_id,
                        item_tempoArmazenamentoDados,
                        item_tempoArmazenamentoDadosUn):

    template_ids = ''
    for template in templates:
        template_ids = template_ids + ('_template_id:' + str(template.id))

    intervalo_id = None

    novoIntervalo = IntervalSchedule(every=1, period='minutes')

    intervalosCadastrados = IntervalSchedule.objects.all()

    for intervalo in intervalosCadastrados:
        if (intervalo.every == novoIntervalo.every) and (intervalo.period == novoIntervalo.period):
            intervalo_id = intervalo.id
            print('ACHEI UM INTERVALO NO BD')

    if intervalo_id is None:
        novoIntervalo.save()
        intervalo_id = novoIntervalo.id
        print('NÃO ACHEI UM INTERVALO E SALVEI NO BD')

    novaTask = PeriodicTask(
        name='CLEANDATATASK=' + host_nomeTabela_snmpGet + str(template_ids) + '_item_id:' + str(item_id),
        task='hosts.tasks.task_clean_data',
        args='[' + '"' + str(item_id) + '", "' + str(item_tempoArmazenamentoDados) + '", "' + item_tempoArmazenamentoDadosUn + '", "' + host_nomeTabela_snmpGet + '"]',
        kwargs='{}',
        enabled=1,
        interval_id=intervalo_id,
        one_off=0,
        headers='{}')
    novaTask.save()
    print('CRIEI UMA NOVA TAREFA')
