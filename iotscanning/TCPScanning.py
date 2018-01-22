import iotscanning
from iotscanning import HTTPFetcher
from iotscanning.PortScanner import PortScanner
from iotscanning.LoginCheckSSH import LoginCheckSSH
from iotscanning.HTTPDeviceFinder import HTTPDeviceFinder
from iotscanning.LoginCheckHTTP import LoginCheckHTTP
from iotscanning.ResponseHandler import ResponseHandler

class TCPScanning():
    """
    Methods to check tcp connections for vulnerabilities.
    """
    def tcp_requirements_met(self):
        """
        Check if all required arguments were given.
        :return: bool
        """
        if iotscanning.IP_ADDRESS_LIST and iotscanning.DEVICES:
            return True
        else:
            return False


    def scan_tcp(self):
        '''
        Performs tcp scanning for each given ip address.
        :return: None
        '''
        port_scanner = PortScanner()
        for ip in iotscanning.IP_ADDRESS_LIST:
            print("\nScanning hosts with ip {0} ...".format(ip))
            scan_results = port_scanner.scan_ports(ip)
            for port in scan_results.keys():
                if self.is_http(scan_results[port]):
                    self.check_http(ip, port)
                elif self.is_ssh(scan_results[port]):
                    self.check_ssh(ip, port)
                else:
                    if iotscanning.VERBOSE:
                        print("Could not check port {0} because the service {1} is not supported.".format(port, scan_results[
                            port]))
        print("-------------------------------------------------")


    def is_http(self, protocol):
        if protocol == 'http':
            return True
        else:
            return False


    def is_ssh(self, protocol):
        if protocol == 'ssh':
            return True
        else:
            return False


    def check_http(self, ip, port):
        """
        Checks http webserver for the use of standard passwords.
        :param ip: int
        :param port: int
        :return: None
        """
        if iotscanning.VERBOSE:
            print("\nScanning http...")
        url = HTTPFetcher.compose_url(ip, port)
        response = HTTPFetcher.fetch(url)
        device_finder = HTTPDeviceFinder(response)
        response_handler = ResponseHandler()
        if response_handler.is_available(response):
            device = device_finder.search_for_device()
            if not device:
                print("No matching device found.")
            else:
                login_check = LoginCheckHTTP(device, url)
                login_check.check_login()


    def check_ssh(self, ip, port):
        """
        Checks ssh server for the use of standard passwords.
        :param ip: int
        :param port: int
        :return: None
        """
        if iotscanning.VERBOSE:
            print("\nScanning ssh...")
        login_possible = False
        brute_force_successful = False
        login_check = LoginCheckSSH()
        for login in iotscanning.DEVICES['ssh']['list']:
            login_possible = login_check.login_check(ip, port, iotscanning.DEVICES['ssh']['list'][login]['username'],
                                                       iotscanning.DEVICES['ssh']['list'][login]['password'])
            if login_possible:
                break
        if not login_possible:
            for wordlist in iotscanning.DEVICES['ssh']['wordlists']:
                brute_force_successful = login_check.bruteforce_ssh(ip, port,
                                                                      iotscanning.DEVICES['ssh']['wordlists'][wordlist])
                if brute_force_successful:
                    break
            if not brute_force_successful:
                print("Could not log into ssh with any default password.")
