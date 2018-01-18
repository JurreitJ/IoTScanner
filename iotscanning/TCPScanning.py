import iotscanning
from iotscanning import HTTPFetcher
from iotscanning.PortScanner import PortScanner
from iotscanning import LoginCheckSSH
from iotscanning.HTTPDeviceFinder import HTTPDeviceFinder
from iotscanning.LoginCheckHTTP import LoginCheckHTTP
from iotscanning.ResponseHandler import ResponseHandler


def tcp_requirements_met():
    if iotscanning.IP_ADDRESS_LIST and iotscanning.DEVICES:
        return True
    else:
        return False


def scan_tcp():
    '''
    Performs tcp scanning for each given ip address.
    :return:
    '''
    port_scanner = PortScanner()
    for ip in iotscanning.IP_ADDRESS_LIST:
        print("\nScanning hosts with ip {0} ...".format(ip))
        scan_results = port_scanner.scan_ports(ip)
        for port in scan_results.keys():
            if is_http(scan_results[port]):
                check_http(ip, port)
            elif is_ssh(scan_results[port]):
                check_ssh(ip, port)
            else:
                if iotscanning.VERBOSE:
                    print("Could not check port {0} because the service {1} is not supported.".format(port, scan_results[
                        port]))
    print("-------------------------------------------------")


def is_http(protocol):
    if protocol == 'http':
        return True
    else:
        return False


def is_ssh(protocol):
    if protocol == 'ssh':
        return True
    else:
        return False


def check_http(ip, port):
    if iotscanning.VERBOSE:
        print("\nScanning http...")
    url = HTTPFetcher.compose_url(ip, port)
    response = HTTPFetcher.fetch(url)
    device_finder = HTTPDeviceFinder(url)
    response_handler = ResponseHandler()
    if response_handler.is_available(response):
        device = device_finder.search_for_device(response)
        if not device:
            print("No matching device found.")
        else:
            login_check = LoginCheckHTTP(device, url)
            login_check.check_login()


def check_ssh(ip, port):
    if iotscanning.VERBOSE:
        print("\nScanning ssh...")
    login_possible = False
    brute_force_successful = False
    for login in iotscanning.DEVICES['ssh']['list']:
        login_possible = LoginCheckSSH.login_check(ip, port, iotscanning.DEVICES['ssh']['list'][login]['username'],
                                                   iotscanning.DEVICES['ssh']['list'][login]['password'])
        if login_possible:
            break
    if not login_possible:
        for wordlist in iotscanning.DEVICES['ssh']['wordlists']:
            brute_force_successful = LoginCheckSSH.bruteforce_ssh(ip, port,
                                                                  iotscanning.DEVICES['ssh']['wordlists'][wordlist])
            if brute_force_successful:
                break
        if not brute_force_successful:
            print("Could not log into ssh with any default password.")
