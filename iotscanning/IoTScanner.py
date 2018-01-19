import sys

import iotscanning
from iotscanning import TCPScanning
from iotscanning import ZigbeeScanning
from iotscanning.ArgumentHandler import ArgumentHandler


def main():
    """
    This tool searches for vulnerabilities in SmartHome devices.
    """
    argument_handler = ArgumentHandler()
    argument_handler.parse_arguments_to_constants()
    if iotscanning.VERBOSE:
        argument_handler.print_arguments()
    if TCPScanning.tcp_requirements_met():
        TCPScanning.scan_tcp()
    if ZigbeeScanning.zb_requirements_met():
        ZigbeeScanning.scan_zb()
    if not (TCPScanning.tcp_requirements_met() or ZigbeeScanning.zb_requirements_met()):
        print("\nMust specify either tcp or zigbee scanning arguments.")
        sys.exit(2)


if __name__ == "__main__":
    main()
