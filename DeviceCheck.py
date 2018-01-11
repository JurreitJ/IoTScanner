"""
Checks, whether the program can connect to a web server
or ssh server, using known standard credentials
"""

import HTTPHandler
import SSHCheck
import ZigbeeScanning
from HTTPCheck import HTTPCheck


def check_tcp(ip, scanresults, devices):
    '''
    Check device security via tcp
    :param ip:
    :param scanresults:
    :param devices:
    :return:
    '''
    for port in scanresults.keys():
        print(port)
        if scanresults[port] == 'ssh':
            login_possible = False
            for login in devices['ssh']:
                login_possible = SSHCheck.ssh_check(ip, port, devices['ssh'][login]['username'],
                                                    devices['ssh'][login]['password'])
                if login_possible:
                    break
            if not login_possible:
                print("Could not log into ssh with any default password.")
        elif scanresults[port] == 'http':
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
            print("Could not check port", port, ", because the service is not supported. Service is:",
                  scanresults[port])


def check_zb(zbdata):
    ZigbeeScanning.scan(zbdata)
