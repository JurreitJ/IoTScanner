import re

from iotscanning.ZigbeeDeviceFinder import ZigBeeDeviceFinder
from iotscanning.ZigbeeSniffer import ZigbeeSniffer
import iotscanning
from killerbee3 import *


def __find_transceiver():
    fmt = "{: >14}"
    device = None
    for dev in kbutils.devlist():
        if re.match("^KILLERB", dev[1]):
            device = fmt.format(dev[0])
    if iotscanning.verbose:
        print("Found hardware compatible with killerbee3:", device)
    return device


def __find_zbdevices(kbdevice, loops, delay):
    channel = []
    zbfinder = ZigBeeDeviceFinder(kbdevice, loops, delay)
    zbdata = zbfinder.find_zb()
    if zbdata != None:
        for key in zbdata:
            if not zbdata[key][4] in channel:
                channel.append(zbdata[key][4])
            print(zbdata[key][4])
    del zbfinder
    return channel


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
    kbdevice = __find_transceiver()
    channels_to_sniff = __find_zbdevices(kbdevice, loops, delay)
    if channels_to_sniff.__len__() == 0:
        print("Couldn't find any nearby zigbee devices.")
    else:
        for channel in channels_to_sniff:
            __sniff(kbdevice, file, channel, packet_count)
