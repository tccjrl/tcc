from pysnmp.hlapi import getCmd, SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, \
    ObjectIdentity


# Função que executa o SNMP Request para o dispositivo da rede que se quer capturar o valor do objeto
def snmpGet(ip, oid, community='public', versao_snmp=0, porta=161):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),  # SnmpEngiene() e o objeto central da operaçao e serve como identificador que e atribuido
               # automaticamente nesse exemplo.
               CommunityData(community, mpModel=versao_snmp),  # comunnity e versao do SNMP para enviar no SNMP Request
               UdpTransportTarget((ip, porta)),  # IP e porta de destino para o SNMP Request
               ContextData(),  # Ele é um parâmetro do utilizado somente no SNMPv3 e deve ser testado sua remoção desse
               # projeto
               ObjectType(ObjectIdentity(oid)))  # OID que é passada a classe ObjectIdentity para identificar a OID
        # (se necessário) e ao objeto Object Type para criar uma tupla de valores.
    )

    if errorIndication:  # Retornado quando ocorre erro no servidor local
        return (str(errorIndication))
    elif errorStatus:  # Retornado quando ocorre erro no agente
        return ('%s at %s' % (errorStatus.prettyPrint(),
                              errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:  # Retorno do resultado quando não ocorre erro
            return str(varBind).split(' = ')[1]
