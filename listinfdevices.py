# parse a Windows device driver installer file (.inf) and the pci.ids
# database and produce a list of compatible devices

import argparse
from wininfparser import WinINF, INFsection
import pci_ids
import re
from pprint import pprint as pp

pci_ids_db = pci_ids.read()
# for testing pci_ids parser
#pp(pci_ids_db)
#exit(0)

parser = argparse.ArgumentParser(description='parse a Windows .inf file and list compatible devices')
parser.add_argument('inf_file', help='path of ESI file')
args = parser.parse_args()

InfFile = WinINF()

#Open .inf
InfFile.ParseFile(args.inf_file)

# Get section with PCI vendor and device IDs
s=InfFile['CODESYS.ntamd64']
if s is None:
    print("Error: section not found!")
    sys.exit(-10)

# note that .inf uses uppercase hex but pci.ids uses lowercase

pci_regex = re.compile(r'PCI\\VEN_(?P<vendor>[A-F0-9]{4})&DEV_(?P<device>[A-F0-9]{4})')

for k,v,c in s:
    m = pci_regex.search(v)
    if m:
        vendor_id = m.group('vendor').lower()
        device_id = m.group('device').lower()
        vendor = pci_ids_db.get(vendor_id)
        if vendor:
            device = vendor['devices'].get(device_id)
            if device:
                print(vendor_id, device_id, device['device_name'])
            else:
                print(vendor['vendor'], device_id, "not found")
        else:
            print("vendor", vendor_id, "not found")
