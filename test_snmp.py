from pysnmp.hlapi import *

def snmp_walk(target, port, user, auth_password, priv_password, auth_proto, priv_proto, base_oid):
    iterator = nextCmd(
        SnmpEngine(),
        UsmUserData(user, authKey=auth_password, privKey=priv_password, authProtocol=auth_proto, privProtocol=priv_proto),
        UdpTransportTarget((target, port)),
        ContextData(),
        ObjectType(ObjectIdentity(base_oid)),
        lexicographicMode=False
    )

    result = {}
    for errorIndication, errorStatus, errorIndex, varBinds in iterator:
        if errorIndication:
            print(f"Error Indication: {errorIndication}")
            break
        elif errorStatus:
            print(f"{errorStatus.prettyPrint()} at {errorIndex and varBinds[int(errorIndex) - 1][0] or '?'}")
            break
        else:
            for varBind in varBinds:
                result[str(varBind[0])] = str(varBind[1])

    return result

# Assuming 'auth_password' and 'priv_password' are the actual passwords
if __name__ == '__main__':
    # Configuration parameters
    target = '10.0.0.1'
    port = 161
    user = 'django'
    auth_password = 'django-pass'
    priv_password = 'django-priv'
    auth_proto = usmHMACSHAAuthProtocol
    priv_proto = usmAesCfb128Protocol
    base_oid = '1.3.6.1'  # Adjusted to a more common starting OID

    result = snmp_walk(target, port, user, auth_password, priv_password, auth_proto, priv_proto, base_oid)
    print(result)
