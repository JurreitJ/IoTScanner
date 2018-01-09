from ZigbeeDeviceFinder import ZigBeeDeviceFinder
from killerbee import kbutils
import re
from ZigbeeSniffer import ZigbeeSniffer


class ZigbeeScanning():
    def __init__(self):
        self.kbdevice = self.__find_transceiver()

    def __find_transceiver(self):
        fmt = "{: >14}"
        device = None
        for dev in kbutils.devlist():
            if re.match("^KILLERB", dev[1]):
                device = fmt.format(dev[0])
        return device

    def find_zbdevices(self):
        zbfinder = ZigBeeDeviceFinder(self.kbdevice, 0.0, 0, True)
        zbdata = zbfinder.zbstumbler()

        for key in zbdata:
            print(zbdata[key][0])

    def sniff_zb(self):
        sniffer = ZigbeeSniffer("test.pcap", self.kbdevice)
        sniffer.sniff()
