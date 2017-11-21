import sys, getopt
import json

import PortScanner
import CheckIoTDevice
import IPHandler

def main(argv):
    ipAddressesString = ''
    devConfigInput = ''
    devices = dict()

    try:
        opts, args = getopt.getopt(argv,"hi:c:",["ip=","devCfg="])
    except getopt.GetoptError:
        print ('IoTScanner.py -i <ipAddresses> -c <config file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('IoTScanner.py -i <ipAddresses> -c <config file>')
            sys.exit(0)
        elif opt in ("-i", "--ip"):
            ipAddressesString = arg
        elif opt in ("-c", "--devCfg"):
            devConfigInput = arg
    print ('IPs are', ipAddressesString)
    print ('Config file is', devConfigInput)
    if devConfigInput != "":
       devices = readDevices(devConfigInput)
    else:
        print("Could not find devices configuration.")
        sys.exit(2)
    if ipAddressesString != "":
        ipList = IPHandler.getIPList(ipAddressesString)
    else:
        print("Could not find any ip addresses.")
        sys.exit(2)
    if ipList.__len__() != 0:
        for ip in ipList:
            scanResults = PortScanner.scanPorts(ip)
            if scanResults:
                CheckIoTDevice.check(ip, scanResults, devices)
    else:
        print("IP list is empty.")
        sys.exit(2)


def readDevices(devConfigInput):
    try:
        with open(devConfigInput) as devConfigFile:
            return json.load(devConfigFile)
    except:
        print("Could not load devices.")
        sys.exit(2)




if __name__ == "__main__":
   main(sys.argv[1:])