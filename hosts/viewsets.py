import datetime

from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django_celery_beat.models import PeriodicTask
from rest_framework.response import Response
from rest_framework import mixins, viewsets, status

from funcoes_Tabelas.man_tabelas_itens import criaTabelaSnmpGet, IDENTIFICADOR_TABELA_SNMPGET, \
    FORMATO_DATA_NOME_TABELA_SNMPGET, deletaTabela, pegaDadosDash
from hosts.models import Item, Template, Host
from hosts.serializers import ItemSerializer, TemplateSerializer, HostSerializer
from hosts.tasks import create_task_snmpGet_host_created, create_task_CleanData_host_created, \
    create_task_snmpGet_host_updated, create_task_CleanData_host_updated, create_task_CleanData_template_updated, \
    create_task_snmpGet_template_updated, create_task_snmpGet_template_deleted, create_task_CleanData_template_deleted, \
    create_task_snmpGet_item_updated, create_task_CleanData_item_updated


class ItemViewSet(viewsets.ViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet
                  ):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def update(self, request, pk=None):
        queryset = Template.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        serializer = TemplateSerializer(data=request.data)

        item_nome_old = item.item_nome
        item_oid_old = item.item_oid

        item_tempoArmazenamentoDados_old = item.item_tempoArmazenamentoDados
        item_tempoArmazenamentoDadosUn_old = item.item_tempoArmazenamentoDadosUn

        if serializer.is_valid():
            serializer.save()
            item_intervaloAtualizacao = serializer.data.get("item_intervaloAtualizacao")
            item_intervaloAtualizacaoUn = serializer.data.get("item_intervaloAtualizacaoUn")
            create_task_snmpGet_item_updated.s(item_id=pk,
                                               item_nome_old=item_nome_old,
                                               item_oid_old=item_oid_old,
                                               item_intervaloAtualizacao_old=item_intervaloAtualizacao,
                                               item_intervaloAtualizacaoUn_old=item_intervaloAtualizacaoUn).apply_async(
                countdown=2)

            create_task_CleanData_item_updated.s(item_id=pk,
                                                 item_tempoArmazenamentoDados_old=item_tempoArmazenamentoDados_old,
                                                 item_tempoArmazenamentoDadosUn_old=item_tempoArmazenamentoDadosUn_old).apply_async(
                countdown=4)

            return Response("Item Deleted", status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        queryset = Item.objects.all()
        template = get_object_or_404(queryset, pk=pk)
        periodicTasks = PeriodicTask.objects.filter(name__contains=('item_id:' + str(pk)))

        template.delete()

        for periodicTask in periodicTasks:
            periodicTask.delete()

        return Response("Item Deleted", status=status.HTTP_200_OK)


class TemplateViewSet(viewsets.ViewSet,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet
                      ):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer

    def update(self, request, pk=None):
        queryset = Template.objects.all()
        template = get_object_or_404(queryset, pk=pk)
        serializer = TemplateSerializer(data=request.data)
        if serializer.is_valid():
            template.template_nome = serializer.data.get('template_nome')
            template.template_item.set(serializer.data.get('template_item'))
            template.template_observacoes = serializer.data.get('template_observacoes')
            template.save()
            create_task_snmpGet_template_updated.s(template_id=pk,
                                                   template_nome=template.template_nome).apply_async(
                countdown=2)

            create_task_CleanData_template_updated.s(template_id=pk,
                                                     template_nome=template.template_nome).apply_async(
                countdown=4)
            return Response("Template Updated", status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        queryset = Template.objects.all()
        template = get_object_or_404(queryset, pk=pk)
        hosts = Host.objects.filter(host_template__id=pk)

        hosts_ids = []
        for host in hosts:
            hosts_ids.append(host.id)

        template.delete()

        create_task_snmpGet_template_deleted.s(hosts_ids=hosts_ids).apply_async(countdown=2)
        create_task_CleanData_template_deleted.s(hosts_ids=hosts_ids).apply_async(countdown=4)

        return Response("Template Deleted", status=status.HTTP_200_OK)


class HostViewSet(viewsets.ViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet
                  ):
    queryset = Host.objects.all()
    serializer_class = HostSerializer

    def create(self, request):
        request.data['host_nomeTabela_snmpGet'] = str(IDENTIFICADOR_TABELA_SNMPGET +
                                                      datetime.datetime.now().strftime(
                                                          FORMATO_DATA_NOME_TABELA_SNMPGET))
        criaTabelaSnmpGet(request.data['host_nomeTabela_snmpGet'])
        serializer = HostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            host = Host(serializer.data)
            if host.host_status:
                create_task_snmpGet_host_created.s(host_nomeTabela_snmpGet=host.host_nomeTabela_snmpGet,
                                                   host_ip=host.host_ip,
                                                   host_porta=host.host_porta,
                                                   host_status=host.host_status,
                                                   host_community=host.host_community).apply_async(countdown=2)

                create_task_CleanData_host_created.s(host_nomeTabela_snmpGet=host.host_nomeTabela_snmpGet,
                                                     host_ip=host.host_ip,
                                                     host_porta=host.host_porta,
                                                     host_status=host.host_status).apply_async(countdown=2)
            return Response(serializer.data)

    def update(self, request, pk=None):
        queryset = Host.objects.all()
        host = get_object_or_404(queryset, pk=pk)
        serializer = HostSerializer(data=request.data)
        if serializer.is_valid():
            host.host_nome = serializer.data.get('host_nome')
            host.host_ip = serializer.data.get('host_ip')
            host.host_porta = serializer.data.get('host_porta')
            host.host_observacoes = serializer.data.get('host_observacoes')
            host.host_status = serializer.data.get('host_status')
            host.host_community = serializer.data.get('host_community')
            host.host_template.set(serializer.data.get('host_template'))
            host.save()

            create_task_snmpGet_host_updated.s(host_nomeTabela_snmpGet=host.host_nomeTabela_snmpGet,
                                               host_ip=host.host_ip,
                                               host_porta=host.host_porta,
                                               host_status=host.host_status,
                                               host_community=host.host_community).apply_async(countdown=2)

            create_task_CleanData_host_updated.s(host_nomeTabela_snmpGet=host.host_nomeTabela_snmpGet,
                                                 host_ip=host.host_ip,
                                                 host_porta=host.host_porta,
                                                 host_status=host.host_status).apply_async(countdown=4)
            return Response("Host Updated", status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        queryset = Host.objects.all()
        host = get_object_or_404(queryset, pk=pk)
        serializer = HostSerializer(host)

        listaPeriodicTasksCadastradas = PeriodicTask.objects.filter(name__contains=host.host_nomeTabela_snmpGet)
        for periodicTask in listaPeriodicTasksCadastradas:
            periodicTask.delete()
        deletaTabela(host.host_nomeTabela_snmpGet)
        host.delete()
        return Response(serializer.data)


class ChartViewSet(viewsets.ViewSet):

    def list(self, request):

        lista_host_data = []
        queryset = Host.objects.filter(host_status=True)

        for host in queryset:
            host_dict = {}
            lista_itens_dados = []
            host_dict['nome_host'] = host.host_nome

            lista_itens_host_query = Item.objects.filter(
                template__host__host_nomeTabela_snmpGet=host.host_nomeTabela_snmpGet,
                template__host__host_ip=host.host_ip,
                template__host__host_porta=host.host_porta,
                template__host__host_status=host.host_status)

            for item in lista_itens_host_query:
                item_dict = {}
                item_dict['item_nome'] = item.item_nome
                item_dict['item_tipoInformacao'] = item.item_tipoInformacao
                labels_data = pegaDadosDash(tabela_snmpGet=host.host_nomeTabela_snmpGet, id_item=item.id)
                item_dict['labels'] = labels_data[0]
                item_dict['data'] = labels_data[1]
                # começo da cagada
                item_dict['expression'] = item.item_expressaoConversao
                # final da cagada
                lista_itens_dados.append(item_dict)

            host_dict['itens'] = lista_itens_dados

            lista_host_data.append(host_dict)

        data = {'lista_host_data': lista_host_data}

        return JsonResponse(data)
