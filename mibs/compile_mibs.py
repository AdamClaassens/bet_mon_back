import os
import re
from pysmi.reader import FileReader, HttpReader
from pysmi.searcher import AnyFileSearcher
from pysmi.writer import PyFileWriter
from pysmi.parser import SmiStarParser
from pysmi.codegen import PySnmpCodeGen
from pysmi.compiler import MibCompiler


def extract_mib_names(directory):
    mib_names = []
    pattern = re.compile(r'(\S+)\s+DEFINITIONS\s+::=\s+BEGIN')

    # Walk through each file in the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt") or file.endswith(".my"):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Search for MIB name using the regex pattern
                match = pattern.search(content)
                if match:
                    mib_names.append(match.group(1))
                else:
                    print('MIB name not found in file:', filepath)
                # Append file name to mib_names without extention
                # mib_names.append(file.split('.')[0])

    return mib_names

import logging
logging.basicConfig(level=logging.DEBUG)


inputMibDirs = ['/Users/adamc/Documents/GitHub/bet_mon_back/mibs/librenms-mibs-master']
outputPyDir = './compiled-mibs'

all_mib_names = set()  # Use a set to avoid duplicate names

for directory in inputMibDirs:
    mib_names = extract_mib_names(directory)
    all_mib_names.update(mib_names)

mibCompiler = MibCompiler(SmiStarParser(), PySnmpCodeGen(), PyFileWriter(outputPyDir))

# Add sources to MIB compiler
for dir in inputMibDirs:
    mibCompiler.addSources(FileReader(dir))

try:
    # Add remote source
    mibCompiler.addSources(HttpReader('mibs.snmplabs.com', 80, '/asn1/'))

    # Optionally, add MIB searcher for dependencies
    mibCompiler.addSearchers(AnyFileSearcher('/usr/share/snmp/mibs'))
    mibCompiler.addSearchers(AnyFileSearcher('./mibs/librenms-mibs-master'))

    # Compile MIB files. Replace 'IF-MIB', 'JUNIPER-MIB' with your MIBs
    compiledMibs = mibCompiler.compile(*all_mib_names)
    # compiledMibs = mibCompiler.compile('mib-SNMPv2-SMI', 'mib-SNMPv2-TC')

    print('Compiled MIBs:', compiledMibs)

except Exception as e:
    print('MIB compilation failed: %s' % e)
