import re

import iotscanner
from iotscanner.ZigbeeDeviceFinder import ZigBeeDeviceFinder
from iotscanner.ZigbeeSniffer import ZigbeeSniffer
from killerbee3 import *


def __find_transceiver():
    fmt = "{: >14}"
    device = None
    for dev in kbutils.devlist():
        if re.match("^KILLERB", dev[1]):
            device = fmt.format(dev[0])
    if iotscanner.VERBOSE:
        print("Found hardware compatible with killerbee3:", device)
    return device


def __find_zbdevices(kbdevice, loops, delay):
    zbfinder = ZigBeeDeviceFinder(kbdevice, loops, delay)
    channel = zbfinder.find_zb()
    return channel


def __sniff(kbdevice, file, channel, packet_count):
    sniffer = ZigbeeSniffer(file, kbdevice, channel, packet_count)
    sniffer.sniff_packets()
    sniffer.sniff_key()
    del sniffer


def scan_zb():
    zb_capturefile = iotscanner.ZB_CAPTURE_FILE
    zb_packet_count = iotscanner.ZB_PACKET_COUNT
    zb_channel = iotscanner.ZB_CHANNEL
    zb_loops = iotscanner.ZB_LOOPS
    zb_delay = iotscanner.ZB_DELAY
    kbdevice = __find_transceiver()
    if zb_channel:
        __sniff(kbdevice, zb_capturefile, zb_channel, zb_packet_count)
    else:
        channels_to_sniff = __find_zbdevices(kbdevice, zb_loops, zb_delay)
        if channels_to_sniff is None:
            print("Couldn't find any nearby zigbee devices.")
        else:
            for channel in channels_to_sniff:
                __sniff(kbdevice, zb_capturefile, channel, zb_packet_count)


def zb_requirements_met():
    if iotscanner.ZB_CAPTURE_FILE:
        return True
    else:
        return False
