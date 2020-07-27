from funcoes_Tabelas.man_tabelas_itens import *

dicionario_templates_hosts_ativos = {}

hosts_ativos = listaHostsAtivos()
templates_hosts_ativos = []
listaTemplatesTemp = []

for hosts_ativos in hosts_ativos:
    templates_hosts_ativos = listaTemplatesHostsAtivos(hosts_ativos[0])
    for templates_hosts_ativos in templates_hosts_ativos:
        listaTemplatesTemp.append(templates_hosts_ativos[2])
    dicionario_templates_hosts_ativos[hosts_ativos[0]] = listaTemplatesTemp.copy()
    listaTemplatesTemp.clear()

print(dicionario_templates_hosts_ativos)