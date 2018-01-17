'''
Sniffing tool to sniff zigbee packets;
Mostly copied from killerbees zbdump
'''

import signal
import sys

import killerbee3
from killerbee3 import *


class ZigbeeSniffer():
    def __init__(self, file, devstring, channel=11, count=10):
        try:
            self.kb = KillerBee(device=devstring)
        except KBInterfaceError as e:
            print(("Interface Error: {0}".format(e)))
            sys.exit(-1)
        self.channel = channel
        self.file = file
        self.count = count
        #FIXME:   self.pd = killerbee3.PcapDumper(killerbee3.DLT_IEEE802_15_4, file) TypeError: sequence item 0: expected str instance, bytes found
        self.pd = killerbee3.PcapDumper(datalink=killerbee3.DLT_IEEE802_15_4, savefile=file)

    def interrupt(self, signum, frame, packetcount):
        self.kb.sniffer_off()
        self.kb.close()
        if self.pd:
            self.pd.close()
        print(("{0} packets captured".format(packetcount)))
        sys.exit(0)

    def sniff_packets(self):
        packetcount = 0
        signal.signal(signal.SIGINT, self.interrupt)
        if not self.kb.is_valid_channel(self.channel):
            print("ERROR: Must specify a valid IEEE 802.15.4 channel for the selected device.")
            self.kb.close()
            sys.exit(1)
        self.kb.set_channel(self.channel)
        self.kb.sniffer_on()
        print(("Listening on \'{0}\', link-type DLT_IEEE802_15_4, capture size 127 bytes".format(
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



    def __getnetworkkey(self, packet):
        """
        Look for the presence of the APS Transport Key command, revealing the
        network key value.
        """

        try:
            zmac = Dot154PacketParser()
            znwk = ZigBeeNWKPacketParser()
            zaps = ZigBeeAPSPacketParser()

            # Process MAC layer details
            zmacpayload = zmac.pktchop(packet)[-1]
            if zmacpayload == None:
                return

            # Process NWK layer details
            znwkpayload = znwk.pktchop(zmacpayload)[-1]
            if znwkpayload == None:
                return

            # Process the APS layer details
            zapschop = zaps.pktchop(znwkpayload)
            if zapschop == None:
                return

            # See if this is an APS Command frame
            apsfc = ord(zapschop[0])
            if (apsfc & ZBEE_APS_FCF_FRAME_TYPE) != ZBEE_APS_FCF_CMD:
                return

            # Delivery mode is Normal Delivery (0)
            apsdeliverymode = (apsfc & ZBEE_APS_FCF_DELIVERY_MODE) >> 2
            if apsdeliverymode != 0:
                return

            # Ensure Security is Disabled
            if (apsfc & ZBEE_APS_FCF_SECURITY) == 1:
                return

            zapspayload = zapschop[-1]

            # Check payload length, must be at least 35 bytes
            # APS cmd | key type | key | sequence number | dest addr | src addr
            if len(zapspayload) < 35:
                return

            # Check for APS command identifier Transport Key (0x05)
            if ord(zapspayload[0]) != 5:
                return

            # Transport Key Frame, get the key type.  Network Key is 0x01, no
            # other keys should be sent in plaintext
            if ord(zapspayload[1]) != 1:
                print("Possible key or false positive?")
                return

            # Reverse these fields
            networkkey = zapspayload[2:18][::-1]
            destaddr = zapspayload[19:27][::-1]
            srcaddr = zapspayload[27:35][::-1]
            for x in networkkey[0:15]:
                print("NETWORK KEY FOUND: ",
                sys.stdout.write("%02x:" % ord(x)))
            print ("%02x" % ord(networkkey[15]))
            for x in zapspayload[2:17]:
                print("      (Wireshark): ",
                sys.stdout.write("%02x:" % ord(x)))
            print("%02x" % ord(zapspayload[17]))
            for x in destaddr[0:7]:
                print("  Destination MAC Address: ",
                sys.stdout.write("%02x:" % ord(x)))
            print ("%02x" % ord(destaddr[7]))
            for x in srcaddr[0:7]:
                print("  Source MAC Address:      ",
                sys.stdout.write("%02x:" % ord(x)))
            print("%02x" % ord(srcaddr[7]))

        except Exception as e:
            # print e
            return

    def sniff_key(self):
        #FIXME: Works with captured file, but not with sample file;
        print ("Processing %s" % self.file)
        if not os.path.exists(self.file):
            print("ERROR: Input file \"%s\" does not exist." % self.file)
            # Check if the input file is libpcap; if not, assume SNA.
        cap = None
        pr = None
        try:
            pr = PcapReader(self.file)
        except Exception as e:
            if e.args == ('Unsupported pcap header format or version',):
                # Input file was not pcap, open it as SNA
                cap = DainTreeReader(self.file)

        # Following exception
        if cap is None:
            cap = pr
        while 1:
            packet = cap.pnext()
            if packet[1] is None:
                # End of capture
                break
            # Add additional key/password/interesting-stuff here
            self.__getnetworkkey(packet[1])
        cap.close()
        print("Processed captured file.")

    def __del__(self):
        self.kb.close()