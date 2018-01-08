from ZigbeeDeviceFinder import ZigBeeDeviceFinder
from killerbee import kbutils
import re

def find_transceiver():
    fmt = "{: >14}"
    device = None
    for dev in kbutils.devlist():
        if re.match("^KILLERB",dev[1]):
            device = fmt.format(dev[0])
    return device


def find_zbdevices():
    kbdevice = find_transceiver()
    zbfinder = ZigBeeDeviceFinder(kbdevice, 0.0, 0, True)
    zbdata = zbfinder.zbstumbler()

    for key in zbdata:
        print(zbdata[key][0])
