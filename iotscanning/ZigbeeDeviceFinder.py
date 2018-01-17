'''
Transmit beacon request frames to the broadcast address while
channel hopping to identify ZigBee Coordinator/Router devices.

Originally from killerbee, modified for zigbee scanner;
'''

import signal
import sys
import iotscanning

from killerbee3 import *


class ZigBeeDeviceFinder():
    def __init__(self, devstring, loops, delay=2.0, channel = 11):
        self.delay = delay
        self.channel = channel
        self.txcount = 0
        self.rxcount = 0
        self.loops = loops
        self.devstring = devstring
        self.devices_found = {}
        try:
            self.kb = KillerBee(device=devstring)
        except KBInterfaceError as e:
            print(("Interface Error: {0}".format(e)))
            sys.exit(-1)

    def display_details(self, routerdata):
        stackprofile_map = {0: "Network Specific",
                            1: "ZigBee Standard",
                            2: "ZigBee Enterprise"}
        stackver_map = {0: "ZigBee Prototype",
                        1: "ZigBee 2004",
                        2: "ZigBee 2006/2007"}
        spanid, source, extpanid, stackprofilever, channel = routerdata
        stackprofile = ord(stackprofilever) & 0x0f
        stackver = (ord(stackprofilever) & 0xf0) >> 4

        print("New Network: PANID 0x%02X%02X  Source 0x%02X%02X" % (
        ord(spanid[0]), ord(spanid[1]), ord(source[0]), ord(source[1])))

        try:
            extpanidstr = ""
            for ind in range(0, 7):
                extpanidstr += "%02x:" % ord(extpanid[ind])
            extpanidstr += "%02X" % ord(extpanid[-1])
            sys.stdout.write("\tExt PANID: " + extpanidstr)
        except IndexError:
            sys.stdout.write("\tExt PANID: Unknown")

        try:
            print("\tStack Profile: %s" % stackprofile_map[stackprofile])
        except KeyError:
            print("\tStack Profile: Unknown (%d)" % stackprofile)

        try:
            print(("\tStack Version: {0}".format(stackver_map[stackver])))
        except KeyError:
            print(("\tStack Version: Unknown ({0})".format(stackver)))

        print(("\tChannel: {0}".format(channel)))

    def response_handler(self, packet):
        #FIXME: Check formats! FCF is wrong!
        d154 = Dot154PacketParser()
        # Chop the packet up
        pktdecode = d154.pktchop(packet)

        print("pktdecode:", pktdecode[0])

        # Byte-swap the frame control field
        fcf = struct.unpack("<H", pktdecode[0])[0]

        print("should be 0", fcf)

        # Check if this is a beacon frame
        if (fcf & DOT154_FCF_TYPE_MASK) == DOT154_FCF_TYPE_BEACON:
            if iotscanning.verbose:
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
            if not key in self.devices_found:
                if iotscanning.verbose:
                    print("Beacon represents new network.")
                self.devices_found[key] = value
                self.display_details(value)
            return self.devices_found
        elif iotscanning.verbose:
            print(("Received frame is not a beacon (FCF={0}).".format(int.from_bytes(pktdecode[0], sys.byteorder))))
        return None



    def find_zb(self):
        networkdata = None
        # Beacon frame
        beacon = "\x03\x08\x00\xff\xff\xff\xff\x07"
        # Immutable strings - split beacon around sequence number field
        beaconp1 = beacon[0:2]
        beaconp2 = beacon[3:]

        print(("Transmitting and receiving on interface \'{0}\'".format(self.kb.get_dev_info()[0])))

        # Sequence number of beacon request frame
        seqnum = 0

        # Loop injecting and receiving packets
        count = 0
        while count < self.loops:
            if self.channel > 26:
                self.channel = 11
                count += 1

            if seqnum > 255:
                seqnum = 0

            if iotscanning.verbose:
                print(("Setting channel to {0}.".format(self.channel)))
            try:
                self.kb.set_channel(self.channel)
            except Exception as e:
                print(("ERROR: Failed to set channel to {0}. ({1})".format(self.channel, e)))
                sys.exit(-1)

            if iotscanning.verbose:
                print("Transmitting beacon request.")

            beaconinj = ''.join([beaconp1, "%c" % seqnum, beaconp2])

            # Process packets for arg_delay seconds looking for the beacon
            # response frame.
            start = time.time()

            try:
                if iotscanning.verbose:
                    print("Injecting packet.")
                self.txcount += 1
                self.kb.inject(beaconinj)
            except Exception as e:
                print(("ERROR: Unable to inject packet: {0}".format(e)))
                sys.exit(-1)

            while start + self.delay > time.time():
                # Does not block
                recvpkt = self.kb.pnext()
                # Check for empty packet (timeout) and valid FCS
                if recvpkt != None and recvpkt[1]:
                    self.rxcount += 1
                    if iotscanning.verbose:
                        print("Received frame.")  # , time.time()-start
                    networkdata = self.response_handler(recvpkt[0])
            seqnum += 1
            self.channel += 1
            self.kb.sniffer_off()
        return networkdata
