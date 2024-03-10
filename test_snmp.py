from pysnmp.hlapi import *
from pysnmp.smi import builder, view, compiler, rfc1902

def SnmpWalk():
    # Create a MIB builder
    mibBuilder = builder.MibBuilder()

    # Add MIB compiler
    compiler.addMibCompiler(mibBuilder, sources=['file://./mibs/librenms-mibs-master'])

    # Load MIBs
    mibBuilder.loadModules('IF-MIB', 'JUNIPER-MIB')
    mibViewController = view.MibViewController(mibBuilder)

    iterator = nextCmd(
        SnmpEngine(),
        UsmUserData('usr-md5-none', 'django'),
        UdpTransportTarget(('10.0.0.1', 161)),
        ContextData(),
        ObjectType(ObjectIdentity('JUNIPER-MIB').addAsn1MibSource('file://./mibs/librenms-mibs-master')),
        lookupMib=False  # This tells pysnmp not to attempt automatic MIB resolution
    )

    for errorIndication, errorStatus, errorIndex, varBinds in iterator:

        if errorIndication:
            print(errorIndication)
            break

        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            break

        else:
            for varBind in varBinds:
                print(' = '.join([x.prettyPrint() for x in varBind]))
    pass


if __name__ == '__main__':
    SnmpWalk()