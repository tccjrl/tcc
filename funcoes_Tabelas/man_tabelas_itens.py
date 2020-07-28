import os.path
import sqlite3

caminho_bancoDeDados = r'C:\Users\johny\OneDrive\tcc\db.sqlite3'

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
                  'data varchar(24) NOT NULL, '
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
