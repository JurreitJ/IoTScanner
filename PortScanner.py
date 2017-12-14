import nmap


def scan_ports(ip):
    open_ports = dict()
    scanner = nmap.PortScanner()
    scanner.scan(ip, arguments="-Pn")  # max port 65535
    if scanner.all_hosts().__len__() == 0:
        print("Could not find any hosts at ip:", ip)
    else:
        host_state = scanner[ip].state()
        if host_state == "up":
            ports = scanner[ip]['tcp'].keys()
            for port in ports:
                port_state = scanner[ip]['tcp'][port]['state']
                if port_state == 'open':
                    print("Port ", port, " is open.")
                    service = scanner[ip]['tcp'][port]['name']
                    if service == 'http':
                        open_ports[port] = 'http'
                    elif service == 'http-proxy':
                        open_ports[port] = 'http'
                    elif service == 'https':
                        open_ports[port] = 'https'
                    elif service == 'https-proxy':
                        open_ports[port] = 'https'
                    else:
                        open_ports[port] = str(service)
                else:
                    print("Port ", port, " is ", port_state)
            if not open_ports:
                print("Could not find any open ports for host at ", ip)
        else:
            print("Host at ip: ", ip, " is probably down. State is: ", host_state)
    return open_ports
