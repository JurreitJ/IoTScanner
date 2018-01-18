"""
Functions to scan tcp ports, using nmap
"""

import nmap

class PortScanner():

    def __init__(self):
        self.open_ports = dict()

    def scan_ports(self, ip):
        scanner = nmap.PortScanner()
        scanner.scan(ip, arguments="-sT -Pn")  # max port 65535; try -Pn if scan fails;
        if scanner.all_hosts().__len__() == 0:
            print("Could not find any hosts at ip:", ip)
        else:
            if self.is_up(scanner[ip]):
                self.retrieve_open_ports_with_service(scanner[ip])
            else:
                print("Host at ip {0} is {1}.".format(ip, scanner[ip].state()))
        if not self.open_ports:
            print("Could not find any open ports for host at ", ip)
        return self.open_ports


    def retrieve_open_ports_with_service(self, host):
        ports = host['tcp'].keys()
        for port in ports:
            port_data = host['tcp'][port]
            if self.is_open(port_data):
                print("Port {0} is open.".format(port))
                service = port_data['name']
                self.make_port_service_dict(service, port)
            else:
                print("Port {0} is [1}.".format(port, port_data['state']))


    def make_port_service_dict(self, service, port):
        if service == 'http':
            self.open_ports[port] = 'http'
        elif service == 'http-proxy':
            self.open_ports[port] = 'http'
        elif service == 'https':
            self.open_ports[port] = 'https'
        elif service == 'https-proxy':
            self.open_ports[port] = 'https'
        else:
            self.open_ports[port] = str(service)

    def is_open(self, port):
        if port['state'] == 'open':
            return True
        else:
            return False

    def is_up(self, host):
        if host.state() == "up":
            return True
        else:
            return False