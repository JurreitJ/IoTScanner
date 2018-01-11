'''
Transmit beacon request frames to the broadcast address while
channel hopping to identify ZigBee Coordinator/Router devices.

Originally from killerbee, modified for zigbee scanner;
'''

import signal
import sys

from killerbee import *


class ZigBeeDeviceFinder():
    def __init__(self, devstring, loops, delay=2.0, channel = 11, verbose=False, ignore=False):
        self.delay = delay
        self.channel = channel
        self.verbose = verbose
        self.ignore = ignore
        self.txcount = 0
        self.rxcount = 0
        self.loops = loops
        try:
            self.kb = KillerBee(device=devstring)
        except KBInterfaceError as e:
            print(("Interface Error: {0}".format(e)))
            sys.exit(-1)

    def response_handler(self, stumbled, packet):
        d154 = Dot154PacketParser()
        # Chop the packet up
        pktdecode = d154.pktchop(packet)

        # Byte-swap the frame control field
        fcf = struct.unpack("<H", pktdecode[0])[0]

        # Check if this is a beacon frame
        if (fcf & DOT154_FCF_TYPE_MASK) == DOT154_FCF_TYPE_BEACON:
            if self.verbose:
                print("Received frame is a beacon.")

            # The 6th element offset in the Dot154PacketParser.pktchop() method
            # contains the beacon data in its own list.  Extract the Ext PAN ID.
            spanid = pktdecode[4][::-1]
            source = pktdecode[5][::-1]
            beacondata = pktdecode[6]
            extpanid = beacondata[6][::-1]
            stackprofilever = beacondata[4]

            key = ''.join([spanid, source])
            value = [spanid, source, extpanid, stackprofilever, self.channel]
            if not key in stumbled:
                if self.verbose:
                    print("Beacon represents new network.")
                stumbled[key] = value
            return stumbled
        if self.verbose:
            print(("Received frame is not a beacon (FCF={0}).".format(pktdecode[0].encode('hex'))))
        return None

    def interrupt(self, signum, frame):
        self.kb.sniffer_off()
        self.kb.close()
        print(("\n{0} packets transmitted, {1} responses.".format(self.txcount, self.rxcount)))
        sys.exit(0)

    def find_zb(self):
        #FIXME: random USB ERROR
        networkdata = None
        stumbled = {}
        # Beacon frame
        beacon = "\x03\x08\x00\xff\xff\xff\xff\x07"
        # Immutable strings - split beacon around sequence number field
        beaconp1 = beacon[0:2]
        beaconp2 = beacon[3:]

        signal.signal(signal.SIGINT, self.interrupt)
        print(("Transmitting and receiving on interface \'{0}\'".format(self.kb.get_dev_info()[0])))

        # Sequence number of beacon request frame
        seqnum = 0

        self.kb.set_channel(self.channel)

        # Loop injecting and receiving packets
        count = 0
        while count <= self.loops:
            if self.channel > 26:
                self.channel = 11

            if seqnum > 255:
                seqnum = 0

            if not self.channel:
                if self.verbose:
                    print(("Setting channel to {0}.".format(self.channel)))
                try:
                    self.kb.set_channel(self.channel)
                except Exception as e:
                    print(("ERROR: Failed to set channel to {0}. ({1})".format(self.channel, e)))
                    sys.exit(-1)

            if self.verbose:
                print("Transmitting beacon request.")

            beaconinj = ''.join([beaconp1, "%c" % seqnum, beaconp2])

            # Process packets for arg_delay seconds looking for the beacon
            # response frame.
            start = time.time()

            try:
                self.txcount += 1
                self.kb.inject(beaconinj)
            except Exception as e:
                print(("ERROR: Unable to inject packet: {0}".format(e)))
                sys.exit(-1)

            while (start + self.delay > time.time()):
                # Does not block
                recvpkt = self.kb.pnext()
                # Check for empty packet (timeout) and valid FCS
                if recvpkt != None and recvpkt[1]:
                    self.rxcount += 1
                    if self.verbose:
                        print("Received frame.")  # , time.time()-start
                    networkdata = self.response_handler(stumbled, recvpkt[0])
            seqnum += 1
            count += 1
            if not self.channel:
                self.channel += 1
        return networkdata
