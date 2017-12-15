"""
Searches for web and ssh servers with default passwords
and zigbee vulnerabilities in IoT devices
"""

import getopt
import sys

import DeviceCheck
import DeviceManager
import IPHandler
import PortScanner


def main(argv):
    ip_addresses_string = ''
    dev_config_input = ''

    try:
        opts, args = getopt.getopt(argv, "hi:c:", ["ip=", "devCfg="])
    except getopt.GetoptError:
        print('IoTScanner.py -i <ipAddresses> -c <config file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('IoTScanner.py -i <ipAddresses> -c <config file>')
            sys.exit(0)
        elif opt in ("-i", "--ip"):
            ip_addresses_string = arg
        elif opt in ("-c", "--devCfg"):
            dev_config_input = arg
    print('IPs are', ip_addresses_string)
    print('Config file is', dev_config_input)
    if dev_config_input != "":
        devices = DeviceManager.read_devices(dev_config_input)
    else:
        print("Could not find devices configuration.")
        sys.exit(2)
    if ip_addresses_string != "":
        ip_list = IPHandler.get_ip_list(ip_addresses_string)
        for ip in ip_list:
            scan_results = PortScanner.scan_ports(ip)
            if scan_results:
                DeviceCheck.check(ip, scan_results, devices)
    else:
        print("Could not find any ip addresses.")
        sys.exit(2)




if __name__ == "__main__":
    main(sys.argv[1:])
