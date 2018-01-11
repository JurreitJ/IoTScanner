import re

from iotscanning.ZigbeeDeviceFinder import ZigBeeDeviceFinder
from iotscanning.ZigbeeSniffer import ZigbeeSniffer
import iotscanning
from killerbee import *


def __find_transceiver():
    fmt = "{: >14}"
    device = None
    for dev in kbutils.devlist():
        if re.match("^KILLERB", dev[1]):
            device = fmt.format(dev[0])
    if iotscanning.verbose:
        print("Found hardware compatible with killerbee:", device)
    return device


def __find_zbdevices(kbdevice, loops, delay):
    zbfinder = ZigBeeDeviceFinder(kbdevice, loops, delay)
    zbdata = zbfinder.find_zb()
    """for key in zbdata:
        print(zbdata[key][0])"""
    print("Hallo", zbdata)
    del zbfinder


def __sniff(kbdevice, file, channel, packet_count):
    sniffer = ZigbeeSniffer(file, kbdevice, channel, packet_count)
    sniffer.sniff_packets()
    sniffer.sniff_key()
    del sniffer


def scan(zbdata):
    file = zbdata["sniffing"]["file"]
    packet_count = zbdata["sniffing"]["packet_count"]
    loops = zbdata["device_search"]["loops"]
    delay = zbdata["device_search"]["delay"]
    # TODO: Retrieve channel from found devices;
    channel = 11
    kbdevice = __find_transceiver()
    #__find_zbdevices(kbdevice, loops, delay)
    __sniff(kbdevice, file, channel, packet_count)
