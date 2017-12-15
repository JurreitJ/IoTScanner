"""
Identifies IoT devices, using the given ip address,
and checks, whether the program can connect to a web server
or ssh server, using known standard credentials
"""

import CheckLogin
import DeviceIdentifier
import Fetcher
import SSHCheck


def check(ip, scanresults, devices):
    # TODO: Programm springt aus der Schleife, nach Überprüfung von HTTP;
    # TODO: Use lambdas;
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
            url = compose_url(ip, port)
            response = Fetcher.fetch(url)
            if type(response) is int:
                if response == 401:
                    devtype = DeviceIdentifier.search_for_devtype(response, devices)
                    return CheckLogin.check_login(url, devtype)
                elif response == 404:
                    print("cannot find dev type for ", url, " due to 404 response.")
                elif response == 595:
                    print("device ", url, ": failed to establish TCP connection.")
                else:
                    print("unexpected status code:", response)
            elif response.getcode() == 200:
                devtype = DeviceIdentifier.search_for_devtype(response, devices)
                if not devtype:
                    print("No matching device found.")
                else:
                    return CheckLogin.check_login(url, devtype)
            else:
                print("unexpected response: ", response)
        else:
            print("Could not check port", port, ", because the service is not supported. Service is:",
                  scanresults[port])


def compose_url(ip, port):
    port_str = str(port)
    url_str = "http://" + ip + ":" + port_str
    return url_str
