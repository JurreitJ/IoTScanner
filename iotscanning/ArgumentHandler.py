import argparse

import iotscanning
from iotscanning.DeviceDataHandler import DeviceDataHandler
from iotscanning import IPHandler


class ArgumentHandler():
    """
    Handles command line arguments.
    """
    def __init__(self):
        """
        Parses command line arguments into a python variable.
        """
        _parser = argparse.ArgumentParser()
        _parser.add_argument('-i', '--ip', dest='ip_address', action='store', default=None,
                             help="IP address or IP address range to be scanned. Format: ['127.0.0.1' | '127.0.0.1,192.168.124.0' | '127.0.0.1-127.0.0.200']")
        _parser.add_argument('-f', '--devices', dest='devices_cfg', action='store', default=None,
                             help="Path to configuration file of devices.")
        _parser.add_argument('-cf', '--capturefile', dest='zb_capture_file', action='store', default=None,
                             help="Path to capture file. Requires sudo and special hardware.")
        _parser.add_argument('-l', '--loops', dest='zb_loops', action='store', default=2, type=int,
                             help="How many different sequences should be tried, when searching for zigbee devices."
                                  "Defaults to 2, if nothing is specified.")
        _parser.add_argument('-d', '--delay', dest='zb_delay', action='store', default=2.0, type=float,
                             help="The delay for sending beacon requests, while searching for zigbee devices."
                                  "Defaults to 2.0, if nothing is specified.")
        _parser.add_argument('-p', '--packetcount', dest='zb_packet_count', action='store', default=100, type=int,
                             help="How many packets should be captured, while scanning zigbee network."
                                  "Defaults to 100, if nothing is specified.")
        _parser.add_argument('-c', '--channel', dest='zb_channel', action='store', default=None, type=int,
                             help="Define the channel to sniff the zigbee network."
                                  "If nothing is specified, IoTScanner searches for used channels of nearby "
                                  "zigbee devices.")
        _parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False,
                             help="Verbose. Defaults to False.")
        self.args = _parser.parse_args()

    def parse_arguments_to_constants(self):
        """
        Parses arguments into constants of the package.
        :return: None
        """
        iotscanning.IP_ADDRESS_LIST = self.__get_ip_addresses(self.args.ip_address)
        iotscanning.DEVICES = self.__get_devices(self.args.devices_cfg)
        iotscanning.ZB_CAPTURE_FILE = self.args.zb_capture_file
        iotscanning.ZB_LOOPS = self.args.zb_loops
        iotscanning.ZB_DELAY = self.args.zb_delay
        iotscanning.ZB_PACKET_COUNT = self.args.zb_packet_count
        iotscanning.ZB_CHANNEL = self.args.zb_channel
        iotscanning.VERBOSE = self.args.verbose

    def print_arguments(self):
        """
        Prints the read arguments.
        :return: None
        """
        print('\nIPs are', iotscanning.IP_ADDRESS_LIST)
        print('Path to devices configuration file is', self.args.devices_cfg)
        print('Path to ZigBee capture file is', iotscanning.ZB_CAPTURE_FILE)
        print('ZigBee device search loops are', iotscanning.ZB_LOOPS)
        print('ZigBee beacon request delay is', iotscanning.ZB_DELAY)
        print('ZigBee packet count is', iotscanning.ZB_PACKET_COUNT)
        print('ZigBee channel is', iotscanning.ZB_CHANNEL)

    def __get_devices(self, devices_cfg):
        """
        Loads device data from the given configuration file.
        :param devices_cfg:
        :return: dict
        """
        if devices_cfg:
            device_handler = DeviceDataHandler()
            return device_handler.read_devices(devices_cfg)
        else:
            return None

    def __get_ip_addresses(self, ip_address_string):
        """
        Get ip addresses in a list.
        :param ip_address_string:
        :return: list
        """
        if ip_address_string:
            return IPHandler.get_ip_list(ip_address_string)
        else:
            return None
