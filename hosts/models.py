from django.db import models

# Lista de formatos de informação retornada pelo snmp_get.py
TIPOS_DE_INFORMACAO_RETORNADA_SNMP_GET = [
    ('NI', 'Numérico(Inteiro)'),
    ('ND', 'Numérico(Decimal)'),
    ('CH', 'Caracter'),
    ('LG', 'Log'),
    ('TX', 'Texto')
]
# Lista de unidades do intervado de atualização
UNIDADES_INTERVALO_ATUALIZACAO = [
    ('seconds', 'Segundos'),
    ('minutes', 'Minutos'),
    ('hours', 'Horas'),
    ('days', 'Dias'),
    ('months', 'Meses'),
    ('years', 'Anos')
]

# Lista de unidades do intervado de atualização
UNIDADES_INTERVALO_ARMAZENAMENTO = [
    ('minutes', 'Minutos'),
    ('hours', 'Horas'),
    ('days', 'Dias'),
    ('months', 'Meses'),
    ('years', 'Anos')
]


# Classe Model que gerencia a tabela Item do banco de dados
class Item(models.Model):
    item_nome = models.CharField(max_length=100)
    item_oid = models.CharField(max_length=100)
    item_tipoInformacao = models.CharField(choices=TIPOS_DE_INFORMACAO_RETORNADA_SNMP_GET, max_length=100)
    item_intervaloAtualizacao = models.PositiveSmallIntegerField(default=1)
    item_intervaloAtualizacaoUn = models.CharField(choices=UNIDADES_INTERVALO_ATUALIZACAO, max_length=100,
                                                   default=UNIDADES_INTERVALO_ATUALIZACAO.__getitem__(1))
    item_tempoArmazenamentoDados = models.PositiveSmallIntegerField(default=90)
    item_tempoArmazenamentoDadosUn = models.CharField(choices=UNIDADES_INTERVALO_ARMAZENAMENTO, max_length=100,
                                                      default=UNIDADES_INTERVALO_ARMAZENAMENTO.__getitem__(2))

    # Função que retorna na view o nome do objeto Item
    def __str__(self):
        return self.item_nome

    # Classe que retorna o nome correto da classe Item no plural
    class Meta:
        verbose_name_plural = 'Itens'


# Classe Model que gerencia a tabela Template do banco de dados
class Template(models.Model):
    template_nome = models.CharField(max_length=100)
    template_item = models.ManyToManyField(Item)
    template_observacoes = models.TextField(null=True, blank=True)

    # Função que retorna na view o nome do objeto Template
    def __str__(self):
        return self.template_nome


# Classe Model que gerencia a tabela Host do banco de dados
class Host(models.Model):
    host_nome = models.CharField(max_length=100)
    host_nomeTabela_snmpGet = models.CharField(max_length=100)
    host_ip = models.GenericIPAddressField(protocol='IPv4', unpack_ipv4=False)
    host_porta = models.PositiveIntegerField(default=161)
    host_template = models.ManyToManyField(Template)
    host_observacoes = models.TextField(null=True, blank=True)
    host_status = models.BooleanField(default=True)

    # Função que retorna na view o nome do objeto Host
    def __str__(self):
        return self.host_nome
