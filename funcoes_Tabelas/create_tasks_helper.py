from hosts.models import Item
from django_celery_beat.models import IntervalSchedule, PeriodicTask


#  Função para capturar os itens de um host
def getItens(host_nomeTabela_snmpGet,  # Nome da tabela que é armazenado as informações capturadas
             host_ip,
             host_porta,
             host_status):
    #  Captura os itens que estão atrelados ao host através dos templates
    itens = Item.objects.filter(template__host__host_nomeTabela_snmpGet=host_nomeTabela_snmpGet,
                                template__host__host_ip=host_ip,
                                template__host__host_porta=host_porta,
                                template__host__host_status=host_status)

    itens_nao_repetidos = []  # lista vazia destinada a ser preenchida com os itens capturados sem repetição
    #  Monta outra lista de itens excluindo os repetidos pois no filtro anterior um item pode estar atrelado duas vezes
    #  ao mesmo host através de templates diferentes
    for item in itens:
        if item not in itens_nao_repetidos:
            itens_nao_repetidos.append(item)

    return itens_nao_repetidos  # Retorna lista de itens não repetidos


#  Função para criar uma task de SNMP-request na tabela django_celery_beat_periodictask
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

    # Monta uma string com os ids dos templates para compor o nome da periodic task snmpget
    template_ids = ''
    for template in templates:
        template_ids = template_ids + ('_template_id:' + str(template.id))

    # Uma flag para identificar se o intervalo de alguns dos itens passados já está cadastrado na tabela
    # django_celery_beat_intervalschedule
    intervalo_id = None

    # Cria um objeto IntervalSchedule com os dados passados na função
    novoIntervalo = IntervalSchedule(every=item_intervaloAtualizacao, period=item_intervaloAtualizacaoUn)

    # Captura todos os intervalos cadastrados da tabela django_celery_beat_intervalschedule
    intervalosCadastrados = IntervalSchedule.objects.all()

    # Procura um intervalo na lista de todos os intervalos capturados e se achar um igual armazena o id na variável
    # intervalo_id
    for intervalo in intervalosCadastrados:
        if (intervalo.every == novoIntervalo.every) and (intervalo.period == novoIntervalo.period):
            intervalo_id = intervalo.id

    # Se não tiver achado nenhum intervalo na etapa anterior então salva o objeto novoIntervalo e captura a nova ID
    # criada
    if intervalo_id is None:
        novoIntervalo.save()
        intervalo_id = novoIntervalo.id

    # Cria uma nova periodicTask na tabela django_celery_beat_periodictask
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


# =======================================================================================================================
# Função para criar uma task para limpar dados antigos das tabelas dos hosts. (intervalo sem será 5 minutos)
def createTaskCleanData(host_nomeTabela_snmpGet,
                        templates,
                        item_id,
                        item_tempoArmazenamentoDados,
                        item_tempoArmazenamentoDadosUn):
    # Monta uma string com os ids dos templates para compor o nome da periodic task cleandata
    template_ids = ''
    for template in templates:
        template_ids = template_ids + ('_template_id:' + str(template.id))

    # Uma flag para identificar se o intervalo de alguns dos itens passados já está cadastrado na tabela
    # django_celery_beat_intervalschedule
    intervalo_id = None

    # Cria um objeto IntervalSchedule com os dados passados na função
    novoIntervalo = IntervalSchedule(every=5, period='minutes')

    # Captura todos os intervalos cadastrados da tabela django_celery_beat_intervalschedule
    intervalosCadastrados = IntervalSchedule.objects.all()

    # Procura um intervalo na lista de todos os intervalos capturados e se achar um igual armazena o id na variável
    # intervalo_id
    for intervalo in intervalosCadastrados:
        if (intervalo.every == novoIntervalo.every) and (intervalo.period == novoIntervalo.period):
            intervalo_id = intervalo.id

    # Se não tiver achado nenhum intervalo na etapa anterior então salva o objeto novoIntervalo e captura a nova ID
    # criada
    if intervalo_id is None:
        novoIntervalo.save()
        intervalo_id = novoIntervalo.id

    # Cria uma nova periodicTask na tabela django_celery_beat_periodictask
    novaTask = PeriodicTask(
        name='CLEANDATATASK=' + host_nomeTabela_snmpGet + str(template_ids) + '_item_id:' + str(item_id),
        task='hosts.tasks.task_clean_data',
        args='[' + '"' + str(item_id) + '", "' + str(
            item_tempoArmazenamentoDados) + '", "' + item_tempoArmazenamentoDadosUn + '", "' + host_nomeTabela_snmpGet + '"]',
        kwargs='{}',
        enabled=1,
        interval_id=intervalo_id,
        one_off=0,
        headers='{}')
    novaTask.save()
