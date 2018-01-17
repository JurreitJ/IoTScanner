"""
Checks, whether the program can connect to a web server
or ssh server, using known standard credentials
"""

from iotscanning import HTTPHandler
from iotscanning import ZigbeeScanning
from iotscanning.HTTPCheck import HTTPCheck
from iotscanning import SSHCheck
import iotscanning


def check_tcp(ip, scanresults, devices):
    '''
    Check device security via tcp
    :param ip:
    :param scanresults:
    :param devices:
    :return:
    '''
    for port in scanresults.keys():
        if scanresults[port] == 'ssh':
            if iotscanning.verbose:
                print("\nScanning ssh...")
            login_possible = False
            brute_force_successful = False
            for login in devices['ssh']['list']:
                login_possible = SSHCheck.ssh_check(ip, port, devices['ssh']['list'][login]['username'],
                                                    devices['ssh']['list'][login]['password'])
                if login_possible:
                    break
            if not login_possible:
                for wordlist in devices['ssh']['wordlists']:
                    brute_force_successful = SSHCheck.bruteforce_ssh(ip, port, devices['ssh']['wordlists'][wordlist])
                    if brute_force_successful:
                        break
                if not brute_force_successful:
                    print("Could not log into ssh with any default password.")
        elif scanresults[port] == 'http':
            if iotscanning.verbose:
                print("\nScanning http...")
            url = HTTPHandler.compose_url(ip, port)
            response = HTTPHandler.fetch(url)
            http_check = HTTPCheck(devices, url)
            if http_check.check_availability(response):
                devtype = http_check.search_for_devtype(response)
                if not devtype:
                    print("No matching device found.")
                else:
                    http_check.check_login(devtype)
        else:
            if iotscanning.verbose:
                print("Could not check port {0} because the service {1} is not supported.".format(port, scanresults[port]))


def check_zb(zbdata):
    ZigbeeScanning.scan(zbdata)
