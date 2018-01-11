import re

from ZigbeeDeviceFinder import ZigBeeDeviceFinder
from ZigbeeSniffer import ZigbeeSniffer
from killerbee import *


def __find_transceiver():
    fmt = "{: >14}"
    device = None
    for dev in kbutils.devlist():
        if re.match("^KILLERB", dev[1]):
            device = fmt.format(dev[0])
    return device


def __find_zbdevices(kbdevice, loops, delay, verbose):
    zbfinder = ZigBeeDeviceFinder(kbdevice, loops, delay, verbose)
    zbdata = zbfinder.find_zb()
    """for key in zbdata:
        print(zbdata[key][0])"""
    print("Hallo", zbdata)
    del zbfinder


def __sniff(kbdevice, file, channel, packet_count, verbose):
    sniffer = ZigbeeSniffer(verbose, file, kbdevice, channel, packet_count)
    sniffer.sniff_packets()
    sniffer.sniff_key(file)
    del sniffer


def scan(zbdata, verbose):
    file = zbdata["sniffing"]["file"]
    packet_count = ["sniffing"]["packet_count"]
    loops = zbdata["device_search"]["loop"]
    delay = zbdata["device_search"]["delay"]
    # TODO: Retrieve channel from found devices;
    channel = 11
    kbdevice = __find_transceiver()
    __find_zbdevices(kbdevice, loops, delay, verbose)
    __sniff(kbdevice, file, channel, packet_count, verbose)
