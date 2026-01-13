

# parse pci.ids
# from https://www.reddit.com/r/learnpython/comments/zbxqa/efficient_parsing_of_pciids_file/

import re

def read():
    re_vendor = re.compile(r'(?P<vendor>[a-z0-9]{4})\s+(?P<vendor_name>.*)')
    re_device = re.compile(r'\t(?P<device>[a-z0-9]{4})\s+(?P<device_name>.*)')
    re_subsys = re.compile(r'\t\t(?P<subvendor>[a-z0-9]{4})\s+(?P<subdevice>[a-z0-9]{4})\s+(?P<subsystem_name>.*)')

    data = {}
    vendor = ''
    device = ''
    
    with open("pci.ids", "rt") as fp:
        for line in fp:
            m = re_vendor.match(line)
            if m:
                d = m.groupdict()
                d['devices'] = {}
                vendor = m.group('vendor')
                data[vendor] = d
            else:
                m = re_device.match(line)
                if m:
                    d = m.groupdict()
                    d['subdevices'] = []
                    device = m.group('device')
                    data[vendor]['devices'][device] = d
                else:
                    m = re_subsys.match(line)
                    if m:
                        data[vendor]['devices'][device]['subdevices'].append(m.groupdict())
    return data
