from django.forms import ModelForm
from .models import Host, Template, Item


# Classe que cria um formulario para o cadastro de hosts e se comunica com a classe Model Host que por sua vez se
# comunica com o banco de dados.
class HostForm(ModelForm):
    class Meta:
        model = Host
        fields = ['host_nome', 'host_nomeTabela_snmpGet', 'host_ip', 'host_porta', 'host_template', 'host_observacoes',
                  'host_status']
        exclude = ['host_nomeTabela_snmpGet']


# Classe que cria um formulario para o cadastro de Templates e se comunica com a classe Model Template que por sua vez
# se comunica com o banco de dados.
class TemplateForm(ModelForm):
    class Meta:
        model = Template
        fields = ['template_nome', 'template_item', 'template_observacoes']


# Classe que cria um formulario para o cadastro de Itens e se comunica com a classe Model Item que por sua vez
# se comunica com o banco de dados.
class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['item_nome', 'item_oid', 'item_tipoInformacao', 'item_intervaloAtualizacao',
                  'item_intervaloAtualizacaoUn', 'item_tempoArmazenamentoDados', 'item_tempoArmazenamentoDadosUn']
