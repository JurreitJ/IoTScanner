from ZigbeeDeviceFinder import ZigBeeDeviceFinder
from killerbee import *
import re
from ZigbeeSniffer import ZigbeeSniffer

def __find_transceiver():
    fmt = "{: >14}"
    device = None
    for dev in kbutils.devlist():
        if re.match("^KILLERB", dev[1]):
            device = fmt.format(dev[0])
    return device

def __find_zbdevices(kbdevice):
    zbfinder = ZigBeeDeviceFinder(kbdevice, 10, channel=11, verbose=True)
    zbdata = zbfinder.find_zb()
    """for key in zbdata:
        print(zbdata[key][0])"""
    print("Hallo", zbdata)
    del zbfinder

def __sniff(kbdevice, file):
    sniffer = ZigbeeSniffer(file, kbdevice)
    #sniffer.sniff_packets()
    sniffer.sniff_key(file)
    del sniffer


def scan():
    kbdevice = __find_transceiver()
    file = "samples/zigbee-network-key-ota.pcap"
    #__find_zbdevices(kbdevice)
    __sniff(kbdevice, file)




