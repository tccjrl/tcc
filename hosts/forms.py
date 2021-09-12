from django.forms import ModelForm, TextInput
from .models import Host, Template, Item


# Classe que cria um formulario para o cadastro de hosts e se comunica com a classe Model Host que por sua vez se
# comunica com o banco de dados.
class HostForm(ModelForm):
    class Meta:
        model = Host
        fields = ['host_nome', 'host_nomeTabela_snmpGet', 'host_ip', 'host_porta', 'host_community', 'host_template', 'host_observacoes',
                  'host_status']
        exclude = ['host_nomeTabela_snmpGet']
        labels = {
            'host_nome': 'Nome',
            'host_ip': 'IP',
            'host_porta': 'Porta',
            'host_community': 'Community',
            'host_template': 'Template(s)',
            'host_observacoes': 'Observações',
            'host_status': 'Ativo'
        }


# Classe que cria um formulario para o cadastro de Templates e se comunica com a classe Model Template que por sua vez
# se comunica com o banco de dados.
class TemplateForm(ModelForm):
    class Meta:
        model = Template
        fields = ['template_nome', 'template_item', 'template_observacoes']
        labels = {
            'template_nome': 'Nome',
            'template_item': 'Item(s)',
            'template_observacoes': 'Observações'
        }


# Classe que cria um formulario para o cadastro de Itens e se comunica com a classe Model Item que por sua vez
# se comunica com o banco de dados.
class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['item_nome', 'item_oid', 'item_tipoInformacao', 'item_intervaloAtualizacao',
                  'item_intervaloAtualizacaoUn', 'item_tempoArmazenamentoDados', 'item_tempoArmazenamentoDadosUn', 'item_expressaoConversao']
        labels = {
            'item_nome': 'Nome',
            'item_oid': 'OID',
            'item_tipoInformacao': 'Formato OID',
            'item_intervaloAtualizacao': 'Frequência',
            'item_intervaloAtualizacaoUn': 'Unidade da frequência',
            'item_tempoArmazenamentoDados': 'Tempo de armazenamento dos dados',
            'item_tempoArmazenamentoDadosUn': 'Unidade do tempo de armazenamento dos dados',
            'item_expressaoConversao': 'Código javascript para conversão dos dados',
        }
        widgets = {
            'item_expressaoConversao': TextInput(attrs={'placeholder': 'Exemplo: {OID}/100.toFixed(2) onde OID é o valor do '
                                                                       'objeto'}),
        }
