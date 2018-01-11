"""
Searches for web and ssh servers with default passwords
and zigbee vulnerabilities in IoT devices
"""

import argparse
import sys

import DataManager
import DeviceCheck
import IPHandler
import PortScanner


def main():
    ip_addresses_string = None
    dev_config_input = None
    verbose = None
    zbcfg = None

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--ip', dest='ip_address', action='store', default=None,
                        help="IP address or IP address range to be scanned. Format: ['127.0.0.1' | '127.0.0.1, 192.168.124.0' | '127.0.0.1 - 127.0.0.200']")
    parser.add_argument('-d', '--devices', dest='devices_cfg', action='store', default=None,
                        help="Path to configuration file of devices.")
    parser.add_argument('-z', '--zigbee', dest='zbcfg', action='store', default=None,
                        help="Path to killerbee scanning configuration file.")
    parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', default=False,
                        help="Verbose")
    args = parser.parse_args()
    ip_addresses_string = args.ip_address
    dev_config_input = args.devices_cfg
    verbose = args.verbose
    zbcfg = args.zbcfg
    print('IPs are', ip_addresses_string)
    print('Config file is', dev_config_input)
    if dev_config_input:
        devices = DataManager.read_devices(dev_config_input)
    else:
        print("Could not find devices configuration.")
        sys.exit(2)
    if ip_addresses_string:
        ip_list = IPHandler.get_ip_list(ip_addresses_string)
        for ip in ip_list:
            scan_results = PortScanner.scan_ports(ip)
            if scan_results:
                DeviceCheck.check_tcp(ip, scan_results, devices)
    else:
        print("Could not find any ip addresses.")
        sys.exit(2)
    if zbcfg:
        zbdata = DataManager.read_zbcfg(zbcfg)
        DeviceCheck.check_zb(zbdata)


if __name__ == "__main__":
    main()
