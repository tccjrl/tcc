from django.shortcuts import render, redirect
from .models import Host, Template, Item
from .forms import HostForm, TemplateForm, ItemForm
from funcoes_Tabelas.man_tabelas_itens import criaTabelaSnmpGet, deletaTabela, FORMATO_DATA_NOME_TABELA_SNMPGET, \
    IDENTIFICADOR_TABELA_SNMPGET
from hosts.tasks import create_task_snmpGet_host_created, create_task_snmpGet_host_updated, create_task_snmpGet_template_updated, create_task_snmpGet_template_deleted, create_task_snmpGet_item_updated, create_task_CleanData_host_created, create_task_CleanData_host_updated, create_task_CleanData_template_updated, create_task_CleanData_template_deleted, create_task_CleanData_item_updated
import datetime
from django_celery_beat.models import PeriodicTask


def homeView(request):
    return render(request, 'hosts/home.html')


# Função responsável por exibir o template listaHost.html que é responsável por exibir a lista de Hosts cadastrados
def listaHost(request):  # Função recebe request do navegador
    data = {'lista_hosts': Host.objects.all()}  # Cria um dicionário chamado 'data' com uma lista dentro chamada
    # 'lista_hosts' que recebe todos os Hosts cadastrados no banco de dados
    return render(request, 'hosts/listaHosts.html', data)  # Retorna a request, template e dicionario criado na função


# Função responsável por exibir o template para cadastrar um novo Host e se comunicar com o Formulario Host do forms.py
def novoHost(request):  # Função recebe request do navegado
    form = HostForm(request.POST or None)  # Cria um formulário que recebe o request.POST quando a função é chamada
    # botão salvar da tela ou None quando chamada para criar um novo Host
    data = {'form': form}  # Cria um dicionario chamado 'data' com uma lista dentro chamada 'form' que recebe o
    # formulario

    if form.is_valid():  # Se o formulário for válido (Conter informações dentro)
        form = form.save()  # Salva formulário primeira vez

        # Preenche o campo host_nomeTabela_snmpGet do novo host criado com o identificador + data e hora
        form.host_nomeTabela_snmpGet = str(IDENTIFICADOR_TABELA_SNMPGET +
                                           datetime.datetime.now().strftime(FORMATO_DATA_NOME_TABELA_SNMPGET))

        criaTabelaSnmpGet(form.host_nomeTabela_snmpGet)  # Chama função para criar nova tabela no banco de dados com o
        # identificador + data e hora

        form.save()  # Salva o formulário segunda vez

        if form.host_status:
            create_task_snmpGet_host_created.s(host_nomeTabela_snmpGet=form.host_nomeTabela_snmpGet,
                                               host_ip=form.host_ip,
                                               host_porta=form.host_porta,
                                               host_status=form.host_status,
                                               host_community=form.host_community).apply_async(countdown=2)

            create_task_CleanData_host_created.s(host_nomeTabela_snmpGet=form.host_nomeTabela_snmpGet,
                                               host_ip=form.host_ip,
                                               host_porta=form.host_porta,
                                               host_status=form.host_status).apply_async(countdown=2)

        return redirect('url_cadastroHost')  # Retorna para a página que lista os Hosts

    return render(request, 'hosts/formularioHost.html', data)  # Renderiza a página para criar um novo Host enviando a
    # request de volta e o formulário vazio


# Função responsável exibir o template para atualizar um novo Host e se comunicar com o Formulário Host do forms.py
def atualizaHost(request, pk):  # Função recebe request do navegador e a ID do Host no banco de dados
    host = Host.objects.get(pk=pk)  # Pega a ID do host selecionado no template
    form = HostForm(request.POST or None, instance=host)  # Cria um formulário que recebe o request.POST quando
    # a função é chamada botão salvar da tela ou None quando chamada para criar um novo Host, também recebe a ID do
    # Host selecionado
    data = {'form': form, 'host': host}  # Cria um dicionário chamado data com as listas forms e hosts

    if form.is_valid():  # Se o formulário for válido (Conter informações dentro)

        form.save()  # Salva o formulário

        create_task_snmpGet_host_updated.s(host_nomeTabela_snmpGet=host.host_nomeTabela_snmpGet,
                                           host_ip=form.cleaned_data.get("host_ip"),
                                           host_porta=form.cleaned_data.get("host_porta"),
                                           host_status=form.cleaned_data.get("host_status"),
                                           host_community=form.cleaned_data.get("host_community")).apply_async(countdown=2)

        create_task_CleanData_host_updated.s(host_nomeTabela_snmpGet=host.host_nomeTabela_snmpGet,
                                           host_ip=form.cleaned_data.get("host_ip"),
                                           host_porta=form.cleaned_data.get("host_porta"),
                                           host_status=form.cleaned_data.get("host_status")).apply_async(countdown=4)

        return redirect('url_cadastroHost')  # Redireciona para a lista de Hosts cadastrados no banco de dados

    return render(request, 'hosts/formularioHost.html', data)  # Renderiza o template com o formulario preenchido para
    # atualizar junto com a request e as informações do formulario


#  Função responsável por deletar um Host do banco de dados
def deletaHost(request, pk):  # Função recebe a request e o ID do Host
    host = Host.objects.get(pk=pk)  # Recebe o Host a ser deletado

    lista_PeriodicTasks_cadastradas = PeriodicTask.objects.filter(name__contains=host.host_nomeTabela_snmpGet)
    for periodicTask in lista_PeriodicTasks_cadastradas:
        periodicTask.delete()

    deletaTabela(host.host_nomeTabela_snmpGet)  # Chama função para deletar a tabela snmpGet do banco de dados
    host.delete()  # deleta o Host
    return redirect('url_cadastroHost')  # Redireciona para a lista de Hosts cadastrados no banco de dados


# =====================================================================================================================
# Função responsável por exibir o template listaTemplate.html que é responsável por exibir a lista de Templates
# cadastrados
def listaTemplate(request):  # Função recebe request do navegador
    data = {'lista_templates': Template.objects.all()}  # Cria um dicionário chamado 'data' com uma lista dentro chamada
    # 'lista_templates' que recebe todos os Templates cadastrados no banco de dados
    return render(request, 'hosts/listaTemplates.html', data)  # Retorna a request, template e dicionario criado na
    # função


# Função responsável por exibir o template para cadastrar um novo Template e se comunicar com o Formulario Template do
# forms.py
def novoTemplate(request):  # Função recebe request do navegado
    form = TemplateForm(request.POST or None)  # Cria um formulário que recebe o request.POST quando a função é chamada
    # pelo botão salvar da tela ou None quando chamada para criar um novo Template
    data = {'form': form}  # Cria um dicionario chamado 'data' com uma lista dentro chamada 'form' que recebe o
    # formulario

    if form.is_valid():  # Se o formulário for válido (Conter informações dentro)
        form.save()  # Salva o formulário
        return redirect('url_listaTemplate')  # Retorna para a página que lista os Templates

    return render(request, 'hosts/formularioTemplate.html', data)  # Renderiza a página para criar um novo Template
    # enviando a request de volta e o formulário vazio


# Função responsável exibir o template para atualizar um novo Template e se comunicar com o Formulário Template do
# forms.py
def atualizaTemplate(request, pk):  # Função recebe request do navegador e a ID do Host no banco de dados
    template = Template.objects.get(pk=pk)  # Pega a ID do template selecionado no template.html
    form = TemplateForm(request.POST or None, instance=template)  # Cria um formulário que recebe o request.POST quando
    # a função é chamada pelo botão salvar da tela ou None quando chamada para criar um novo Template, também recebe a
    # ID do Template selecionado
    data = {'form': form, 'template': template}  # Cria um dicionário chamado data com as listas forms e template

    if form.is_valid():  # Se o formulário for válido (Conter informações dentro)
        form.save()  # Salva o formulário

        create_task_snmpGet_template_updated.s(template_id=pk,
            template_nome=form.cleaned_data.get("template_nome")).apply_async(countdown=2)

        create_task_CleanData_template_updated.s(template_id=pk,
            template_nome=form.cleaned_data.get("template_nome")).apply_async(countdown=4)

        return redirect('url_listaTemplate')  # Redireciona para a lista de Templates cadastrados no banco de dados

    return render(request, 'hosts/formularioTemplate.html', data)  # Renderiza o template com o formulario preenchido
    # para atualizar junto com a request e as informações do formulario


#  Função responsável por deletar um Template do banco de dados
def deletaTemplate(request, pk):  # Função recebe a request e o ID do Template
    template = Template.objects.get(pk=pk)  # Recebe o Template a ser deletado
    hosts = Host.objects.filter(host_template__id=pk)

    hosts_ids = []
    for host in hosts:
        hosts_ids.append(host.id)

    template.delete()  # deleta o Template
    create_task_snmpGet_template_deleted.s(hosts_ids=hosts_ids).apply_async(countdown=2)

    create_task_CleanData_template_deleted.s(hosts_ids=hosts_ids).apply_async(countdown=4)
    return redirect('url_listaTemplate')  # Redireciona para a lista de Templates cadastrados no banco de dados


#  =====================================================================================================================
# Função responsável por exibir o template listaItem.html que é responsável por exibir a lista de Itens
# cadastrados no banco de dados
def listaItem(request):  # Função recebe request do navegador
    data = {'lista_itens': Item.objects.all()}  # Cria um dicionário chamado 'data' com uma lista dentro chamada
    # 'lista_itens' que recebe todos os Itens cadastrados no banco de dados
    return render(request, 'hosts/listaItens.html', data)  # Retorna a request, template e dicionario criado na
    # função


# Função responsável por exibir o template para cadastrar um novo Item e se comunicar com o Formulario Item do
# forms.py
def novoItem(request):  # Função recebe request do navegado
    form = ItemForm(request.POST or None)  # Cria um formulário que recebe o request.POST quando a função é chamada
    # pelo botão salvar da tela ou None quando chamada para criar um novo Item
    data = {'form': form}  # Cria um dicionario chamado 'data' com uma lista dentro chamada 'form' que recebe o
    # formulario

    if form.is_valid():  # Se o formulário for válido (Conter informações dentro)
        form.save()  # Salva o formulário
        return redirect('url_listaItem')  # Retorna para a página que lista os Templates

    return render(request, 'hosts/formularioItem.html', data)  # Renderiza a página para criar um novo Item
    # enviando a request de volta e o formulário vazio


# Função responsável exibir o template para atualizar um novo Item e se comunicar com o Formulário Item do
# forms.py
def atualizaItem(request, pk):  # Função recebe request do navegador e a ID do Item no banco de dados
    item = Item.objects.get(pk=pk)  # Pega a ID do item selecionado no template.html
    item_nome_old = item.item_nome
    item_oid_old = item.item_oid

    item_tempoArmazenamentoDados_old = item.item_tempoArmazenamentoDados
    item_tempoArmazenamentoDadosUn_old = item.item_tempoArmazenamentoDadosUn

    form = ItemForm(request.POST or None, instance=item)  # Cria um formulário que recebe o request.POST quando
    # a função é chamada pelo botão salvar da tela ou None quando chamada para criar um novo Item, também recebe a
    # ID do Item selecionado
    data = {'form': form, 'item': item}  # Cria um dicionário chamado data com as listas forms e item

    if form.is_valid():  # Se o formulário for válido (Conter informações dentro)
        form.save()  # Salva o formulário
        item_intervaloAtualizacao = form.cleaned_data.get("item_intervaloAtualizacao")
        item_intervaloAtualizacaoUn = form.cleaned_data.get("item_intervaloAtualizacaoUn")
        create_task_snmpGet_item_updated.s(item_id=pk,
                                           item_nome_old=item_nome_old,
                                           item_oid_old=item_oid_old,
                                           item_intervaloAtualizacao_old=item_intervaloAtualizacao,
                                           item_intervaloAtualizacaoUn_old=item_intervaloAtualizacaoUn).apply_async(countdown=2)

        create_task_CleanData_item_updated.s(item_id=pk,
                                           item_tempoArmazenamentoDados_old=item_tempoArmazenamentoDados_old,
                                           item_tempoArmazenamentoDadosUn_old=item_tempoArmazenamentoDadosUn_old).apply_async(
            countdown=4)

        return redirect('url_listaItem')  # Redireciona para a lista de Itens cadastrados no banco de dados

    return render(request, 'hosts/formularioItem.html', data)  # Renderiza o template com o formulario preenchido
    # para atualizar junto com a request e as informações do formulario


#  Função responsável por deletar um Item do banco de dados
def deletaItem(request, pk):  # Função recebe a request e o ID do Item
    item = Item.objects.get(pk=pk)  # Recebe o Item a ser deletado
    periodicTasks = PeriodicTask.objects.filter(name__contains=('item_id:' + str(pk)))
    item.delete()  # deleta o item

    for periodicTask in periodicTasks:
        periodicTask.delete()

    return redirect('url_listaItem')  # Redireciona para a lista de Itens cadastrados no banco de dados
