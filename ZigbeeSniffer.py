'''
Sniffing tool to sniff zigbee packets;
'''

import signal
import sys
from killerbee import *
import killerbee

class ZigbeeSniffer():
    def __init__(self, file, devstring, channel = 11, count = 100):
        self.kb = KillerBee(devstring, channel)
        self.channel = channel
        self.file = file
        self.count = count
        self.pd = killerbee.PcapDumper(killerbee.DLT_IEEE802_15_4, file)

    def interrupt(self, signum, frame, packetcount):
        self.kb.sniffer_off()
        self.kb.close()
        if self.pd:
            self.pd.close()
        print(("{0} packets captured".format(packetcount)))
        sys.exit(0)

    def sniff(self):
        packetcount = 0
        signal.signal(signal.SIGINT, self.interrupt)
        if not self.kb.is_valid_channel(self.channel):
            print("ERROR: Must specify a valid IEEE 802.15.4 channel for the selected device.")
            self.kb.close()
            sys.exit(1)
        self.kb.set_channel(self.channel)
        self.kb.sniffer_on()
        print(("zbdump.py: listening on \'{0}\', link-type DLT_IEEE802_15_4, capture size 127 bytes".format(
            self.kb.get_dev_info()[0])))

        rf_freq_mhz = (self.channel - 10) * 5 + 2400
        while self.count != packetcount:
            packet = self.kb.pnext()
            # packet[1] is True if CRC is correct, check removed to have promiscous capture regardless of CRC
            if packet != None:  # and packet[1]:
                packetcount += 1
                if self.pd:
                    self.pd.pcap_dump(packet['bytes'], ant_dbm=packet['dbm'], freq_mhz=rf_freq_mhz)
        self.kb.sniffer_off()
        self.kb.close()
        if self.pd:
            self.pd.close()
        print(("{0} packets captured".format(packetcount)))

