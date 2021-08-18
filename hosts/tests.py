from pysnmp.hlapi import getCmd, SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType,\
    ObjectIdentity


def snmpGet(ip, oid, community='public', versao_snmp=0, porta=161):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(community, mpModel=versao_snmp),
               UdpTransportTarget((ip, porta)),
               ContextData(),
               ObjectType(ObjectIdentity(oid)))
    )

    if errorIndication:
        print("ERROR INDICATION")
        return(str(errorIndication))
    elif errorStatus:
        print("ERROR STATUS")
        return('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        print("VAR BINDS")
        for varBind in varBinds:
            return (' = '.join([x.prettyPrint() for x in varBind])).split(' = ')[1]


print(snmpGet("192.168.0.2", "1.3.6.1.2.1.1.5.0"))