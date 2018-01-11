"""
Searches for web and ssh servers with default passwords
and zigbee vulnerabilities in IoT devices
"""

import argparse
import sys

from iotscanning import DeviceCheck
from iotscanning import IPHandler
from iotscanning import PortScanner
from iotscanning import DataManager
import iotscanning

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', dest='ip_address', action='store', default=None,
                        help="IP address or IP address range to be scanned. Format: ['127.0.0.1' | '127.0.0.1, 192.168.124.0' | '127.0.0.1 - 127.0.0.200']")
    parser.add_argument('-d', '--devices', dest='devices_cfg', action='store', default=None,
                        help="Path to configuration file of devices.")
    parser.add_argument('-z', '--zigbee', dest='zbcfg', action='store', default=None,
                        help="Path to killerbee scanning configuration file. Requires sudo and special hardware.")
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False,
                        help="Verbose")
    args = parser.parse_args()
    ip_addresses_string = args.ip_address
    dev_config_input = args.devices_cfg
    iotscanning.verbose = args.verbose
    zbcfg = args.zbcfg
    if iotscanning.verbose:
        print('IPs are', ip_addresses_string)
        print('Config file is', dev_config_input)
        print('zigbee configuration file is', zbcfg)
        print('verbose is', iotscanning.verbose)
    if dev_config_input and ip_addresses_string:
        devices = DataManager.read_devices(dev_config_input)
        ip_list = IPHandler.get_ip_list(ip_addresses_string)
        for ip in ip_list:
            scan_results = PortScanner.scan_ports(ip)
            if scan_results:
                DeviceCheck.check_tcp(ip, scan_results, devices)
    if zbcfg:
        zbdata = DataManager.read_zbcfg(zbcfg)
        DeviceCheck.check_zb(zbdata)
    if not (dev_config_input or ip_addresses_string or zbcfg):
        print("Must specify either tcp or zigbee scanning arguments.")
        sys.exit(2)


if __name__ == "__main__":
    main()
