from hosts.models import Item
from django_celery_beat.models import IntervalSchedule, PeriodicTask


def getItens(host_nomeTabela_snmpGet,
             host_ip,
             host_porta,
             host_status):
    itens = Item.objects.filter(template__host__host_nomeTabela_snmpGet=host_nomeTabela_snmpGet,
                                template__host__host_ip=host_ip,
                                template__host__host_porta=host_porta,
                                template__host__host_status=host_status)
    return itens

def createTaskSnmpGet(host_nomeTabela_snmpGet,
                      host_ip,
                      host_porta,
                      item_id,
                      item_oid,
                      item_intervaloAtualizacao,
                      item_intervaloAtualizacaoUn):

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


    novaTask = PeriodicTask(name=host_nomeTabela_snmpGet + '_item_id:' + str(item_id),
                            task='hosts.tasks.task_snmp_get',
                            args='[' + '"' + host_ip + '", "' + item_oid + '"]',
                            kwargs='{}',
                            enabled=1,
                            interval_id=intervalo_id,
                            one_off=0,
                            headers='{}')
    novaTask.save()
    print('CRIEI UMA NOVA TAREFA')
