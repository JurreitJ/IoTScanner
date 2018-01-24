import sys

import iotscanner
from iotscanner import ZigbeeScanning
from iotscanner.ArgumentHandler import ArgumentHandler
from iotscanner.TCPScanning import TCPScanning


def main():
    """
    This tool searches for vulnerabilities in SmartHome devices.
    """
    argument_handler = ArgumentHandler()
    argument_handler.parse_arguments_to_constants()
    tcp_scanning = TCPScanning()
    if iotscanner.VERBOSE:
        argument_handler.print_arguments()
    if tcp_scanning.tcp_requirements_met():
        tcp_scanning.scan_tcp()
    if ZigbeeScanning.zb_requirements_met():
        ZigbeeScanning.scan_zb()
    if not (tcp_scanning.tcp_requirements_met() or ZigbeeScanning.zb_requirements_met()):
        print("\nMust specify either tcp or zigbee scanning arguments.")
        sys.exit(2)


if __name__ == "__main__":
    main()
