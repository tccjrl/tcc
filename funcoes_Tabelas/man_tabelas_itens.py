import os.path
import sqlite3
import datetime

caminho_bancoDeDados = r'/home/johny/PycharmProjects/tcc/db.sqlite3'

IDENTIFICADOR_TABELA_SNMPGET = 'snmp_get_'
FORMATO_DATA_NOME_TABELA_SNMPGET = '%d_%m_%Y_%H_%M_%S'


def criaTabelaSnmpGet(nome_tabela_snmpGet):
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
    else:
        return print('Corrija o caminho do banco de dados')


def deletaTabela(nome_tabela):
    if os.path.exists(caminho_bancoDeDados):
        conexao = sqlite3.connect(caminho_bancoDeDados)
        c = conexao.cursor()
        c.execute('DROP TABLE IF EXISTS ' + nome_tabela)

        conexao.close()
    else:
        return print('Corrija o caminho do banco de dados')

def verificaNomeTabela(nomeTabela):
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
    else:
        return print('Corrija o caminho do banco de dados')


def pegaTabelasBD():
    if os.path.exists(caminho_bancoDeDados):
        conexao = sqlite3.connect(caminho_bancoDeDados)
        c = conexao.cursor()
        lista = []
        c.execute("""SELECT name FROM sqlite_master WHERE type='table' ORDER BY name""")

        for reg in c.fetchall():
            lista.append(reg[0])

        conexao.close()
        return lista
    else:
        return print('Corrija o caminho do banco de dados')


def pegaHostsAtivos():
    if os.path.exists(caminho_bancoDeDados):
        conexao = sqlite3.connect(caminho_bancoDeDados)
        c = conexao.cursor()
        lista = []
        c.execute("""SELECT * FROM hosts_host WHERE host_status=True""")

        for reg in c.fetchall():
            lista.append(reg)

        conexao.close()
        return lista
    else:
        return print('Corrija o caminho do banco de dados')


def pegaTemplatesHosts(host_id):
    if os.path.exists(caminho_bancoDeDados):
        conexao = sqlite3.connect(caminho_bancoDeDados)
        c = conexao.cursor()
        lista = []
        c.execute("""SELECT * FROM hosts_host_host_template WHERE host_id=?""", (host_id,))

        for reg in c.fetchall():
            lista.append(reg)

        conexao.close()
        return lista
    else:
        return print('Corrija o caminho do banco de dados')


def pegaItensTemplatesHosts(template_id):
    if os.path.exists(caminho_bancoDeDados):
        conexao = sqlite3.connect(caminho_bancoDeDados)
        c = conexao.cursor()
        lista = []
        c.execute("""SELECT * FROM hosts_template_template_item WHERE template_id=?""", (template_id,))

        for reg in c.fetchall():
            lista.append(reg)

        conexao.close()
        return lista
    else:
        return print('Corrija o caminho do banco de dados')

def insertSnmpGetResult(host_nomeTabela_snmpGet, id_item, nome_item, info):
    if os.path.exists(caminho_bancoDeDados):

        conexao = sqlite3.connect(caminho_bancoDeDados)
        c = conexao.cursor()
        c.execute("INSERT INTO " + host_nomeTabela_snmpGet + " VALUES (NULL," + str(id_item) + ",'" + nome_item + "','" + str(datetime.datetime.now()) + "','" + info + "')")

        conexao.commit()
        conexao.close()


def clean_data(item_id,
               item_tempoArmazenamentoDados,
               item_tempoArmazenamentoDadosUn,
               host_nomeTabela_snmpGet):

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

    if os.path.exists(caminho_bancoDeDados):
        conexao = sqlite3.connect(caminho_bancoDeDados)
        c = conexao.cursor()

        cmdDateTimeSQLite = """'now', 'localtime', '-{} {}'""".format(item_tempoArmazenamentoDados, item_tempoArmazenamentoDadosUn)
        print(cmdDateTimeSQLite)

        cmd = 'DELETE FROM ' + host_nomeTabela_snmpGet + ' WHERE id_item=' + str(item_id) + ' AND data < datetime(' + cmdDateTimeSQLite + ')'
        print(cmd)
        c.execute(cmd)

        conexao.commit()
        conexao.close()

def pegaDadosDash(tabela_snmpGet, id_item, ):
    if os.path.exists(caminho_bancoDeDados):
        conexao = sqlite3.connect(caminho_bancoDeDados)
        c = conexao.cursor()
        dados = []
        labels = []

        c.execute("SELECT data, info FROM %s WHERE id_item=%d" % (tabela_snmpGet, id_item))

        for reg in c.fetchall():
            labels.append(reg[0])
            dados.append(reg[1])

        conexao.close()

        return [labels, dados]
    else:
        return print('Corrija o caminho do banco de dados')
