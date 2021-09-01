import os.path
import sqlite3
import datetime

caminho_bancoDeDados = r'/home/johny/PycharmProjects/tcc/db.sqlite3'  # Caminho do banco de dados

IDENTIFICADOR_TABELA_SNMPGET = 'snmp_get_'  # Prefixo para o nome das tabelas de armazenamento dos hosts
FORMATO_DATA_NOME_TABELA_SNMPGET = '%d_%m_%Y_%H_%M_%S'  # Formato de data e hora para nome das tabelas dos hosts


#  Função para criar tabela de armazenamento quando um host for cadastrado
def criaTabelaSnmpGet(nome_tabela_snmpGet):
    #  Verifica se o caminho passado existe
    if os.path.exists(caminho_bancoDeDados):
        conexao = sqlite3.connect(caminho_bancoDeDados)
        c = conexao.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS ' + nome_tabela_snmpGet +
                  ' ('
                  'id integer NOT NULL PRIMARY KEY AUTOINCREMENT, '
                  'id_item integer NOT NULL, '
                  'nome_item varchar(100) NOT NULL, '
                  'data varchar(60) NOT NULL, '
                  'info varchar(150) NOT NULL)')

        conexao.close()
    else:  # Se o caminho não existir então printa um aviso no console para corrigir o caminho do banco de dados
        return print('Corrija o caminho do banco de dados')


#  Função para deletar tabela no banco de dados quando um host for deletado.
def deletaTabela(nome_tabela):
    # Verifica se o caminho passado existe no banco de dados.
    if os.path.exists(caminho_bancoDeDados):
        conexao = sqlite3.connect(caminho_bancoDeDados)
        c = conexao.cursor()
        c.execute('DROP TABLE IF EXISTS ' + nome_tabela)

        conexao.close()
    else:  # Se o caminho não existir então printa um aviso no console para corrigir o caminho do banco de dados
        return print('Corrija o caminho do banco de dados')


#  Função que verifica de a tabela já existe no banco de dados
def verificaNomeTabela(nomeTabela):
    # Verifica se o caminho passado existe no banco de dados.
    if os.path.exists(caminho_bancoDeDados):
        conexao = sqlite3.connect(caminho_bancoDeDados)
        c = conexao.cursor()

        c.execute("""SELECT count(*) FROM sqlite_master WHERE type='table' AND NAME=?""", (nomeTabela,))
        asn = c.fetchall().__getitem__(0)[0]
        conexao.close()

        if asn == 0:
            return False
        else:
            return True
    else:  # Se o caminho não existir então printa um aviso no console para corrigir o caminho do banco de dados
        return print('Corrija o caminho do banco de dados')


#  Função que captura lista com nome das tabelas do banco de dados
def pegaTabelasBD():
    # Verifica se o caminho passado existe no banco de dados.
    if os.path.exists(caminho_bancoDeDados):
        conexao = sqlite3.connect(caminho_bancoDeDados)
        c = conexao.cursor()
        lista = []
        c.execute("""SELECT name FROM sqlite_master WHERE type='table' ORDER BY name""")

        for reg in c.fetchall():
            lista.append(reg[0])

        conexao.close()
        return lista
    else:  # Se o caminho não existir então printa um aviso no console para corrigir o caminho do banco de dados
        return print('Corrija o caminho do banco de dados')


#  Função que captura hosts ativos da tabela hosts_host
def pegaHostsAtivos():
    # Verifica se o caminho passado existe no banco de dados.
    if os.path.exists(caminho_bancoDeDados):
        conexao = sqlite3.connect(caminho_bancoDeDados)
        c = conexao.cursor()
        lista = []
        c.execute("""SELECT * FROM hosts_host WHERE host_status=True""")

        for reg in c.fetchall():
            lista.append(reg)

        conexao.close()
        return lista
    else:  # Se o caminho não existir então printa um aviso no console para corrigir o caminho do banco de dados
        return print('Corrija o caminho do banco de dados')


#  Função para capturar templates do host passado como parâmetro
def pegaTemplatesHosts(host_id):
    # Verifica se o caminho passado existe no banco de dados.
    if os.path.exists(caminho_bancoDeDados):
        conexao = sqlite3.connect(caminho_bancoDeDados)
        c = conexao.cursor()
        lista = []
        c.execute("""SELECT * FROM hosts_host_host_template WHERE host_id=?""", (host_id,))

        for reg in c.fetchall():
            lista.append(reg)

        conexao.close()
        return lista
    else:  # Se o caminho não existir então printa um aviso no console para corrigir o caminho do banco de dados
        return print('Corrija o caminho do banco de dados')


#  Função para capturar itens do template passado como parâmetro
def pegaItensTemplatesHosts(template_id):
    # Verifica se o caminho passado existe no banco de dados.
    if os.path.exists(caminho_bancoDeDados):
        conexao = sqlite3.connect(caminho_bancoDeDados)
        c = conexao.cursor()
        lista = []
        c.execute("""SELECT * FROM hosts_template_template_item WHERE template_id=?""", (template_id,))

        for reg in c.fetchall():
            lista.append(reg)

        conexao.close()
        return lista
    else:  # Se o caminho não existir então printa um aviso no console para corrigir o caminho do banco de dados
        return print('Corrija o caminho do banco de dados')


#  Função para fazer o insert do resultado do SNMP-request na tabela do banco de dados
def insertSnmpGetResult(host_nomeTabela_snmpGet, id_item, nome_item, info):
    # Verifica se o caminho passado existe no banco de dados.
    if os.path.exists(caminho_bancoDeDados):

        conexao = sqlite3.connect(caminho_bancoDeDados)
        c = conexao.cursor()
        c.execute("INSERT INTO " + host_nomeTabela_snmpGet + " VALUES (NULL," + str(id_item) + ",'" + nome_item + "','" + str(datetime.datetime.now()) + "','" + info + "')")

        conexao.commit()
        conexao.close()

    else:  # Se o caminho não existir então printa um aviso no console para corrigir o caminho do banco de dados
        return print('Corrija o caminho do banco de dados')


# Função para deletar informações antigas da tabela do host no banco de dados
def clean_data(item_id,
               item_tempoArmazenamentoDados,
               item_tempoArmazenamentoDadosUn,
               host_nomeTabela_snmpGet):

    # Switch para converter unidade de tempo para singular
    if (item_tempoArmazenamentoDadosUn == 'seconds'):
        item_tempoArmazenamentoDadosUn = 'second'

    elif (item_tempoArmazenamentoDadosUn == 'minutes'):
        item_tempoArmazenamentoDadosUn = 'minute'

    elif (item_tempoArmazenamentoDadosUn == 'hours'):
        item_tempoArmazenamentoDadosUn = 'hour'

    elif (item_tempoArmazenamentoDadosUn == 'days'):
        item_tempoArmazenamentoDadosUn = 'day'

    elif (item_tempoArmazenamentoDadosUn == 'months'):
        item_tempoArmazenamentoDadosUn = 'month'

    else:
        item_tempoArmazenamentoDadosUn = 'year'

    # Verifica se o caminho passado existe no banco de dados.
    if os.path.exists(caminho_bancoDeDados):
        conexao = sqlite3.connect(caminho_bancoDeDados)
        c = conexao.cursor()

        # Monta parte do comando com o com os filtros de tempo para ser executado no banco de dados
        cmdDateTimeSQLite = """'now', 'localtime', '-{} {}'""".format(item_tempoArmazenamentoDados, item_tempoArmazenamentoDadosUn)

        # Monta comando para deletar as informações da tabela do host cuja data for anterior a passada como parâmetro
        cmd = 'DELETE FROM ' + host_nomeTabela_snmpGet + ' WHERE id_item=' + str(item_id) + ' AND data < datetime(' + cmdDateTimeSQLite + ')'
        c.execute(cmd)

        conexao.commit()
        conexao.close()

    else:  # Se o caminho não existir então printa um aviso no console para corrigir o caminho do banco de dados
        return print('Corrija o caminho do banco de dados')


# Função para do banco de dados as datas e informações de um determinado item
def pegaDadosDash(tabela_snmpGet, id_item, ):
    # Verifica se o caminho passado existe no banco de dados.
    if os.path.exists(caminho_bancoDeDados):
        conexao = sqlite3.connect(caminho_bancoDeDados)
        c = conexao.cursor()
        dados = []
        labels = []

        c.execute("SELECT data, info FROM %s WHERE id_item=%d" % (tabela_snmpGet, id_item))

        #  Monta duas listas com labels e dados da tabela
        for reg in c.fetchall():
            labels.append(reg[0])  # lista com data e horário das informações gravadas na tabela
            dados.append(reg[1])  # lista com valor da OID capturada gravada na tabela

        conexao.close()

        return [labels, dados]
    else:  # Se o caminho não existir então printa um aviso no console para corrigir o caminho do banco de dados
        return print('Corrija o caminho do banco de dados')
