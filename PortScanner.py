import nmap


def scanPorts(ip):
    openPorts = dict()
    scanner = nmap.PortScanner()
    scanner.scan(ip, arguments="-sT") # max port 65535
    if scanner.all_hosts().__len__() == 0:
        print("Could not find any hosts at ip:", ip)
    else:
        hostState = scanner[ip].state()
        if hostState == "up":
            ports = scanner[ip]['tcp'].keys()
            for port in ports:
                portState = scanner[ip]['tcp'][port]['state']
                if portState == 'open':
                    print("Port ", port, " is open.")
                    service = scanner[ip]['tcp'][port]['name']
                    if service == 'http':
                        openPorts[port] = 'http'
                    elif  service == 'http-proxy' :
                        openPorts[port] = 'http'
                    elif service == 'https' :
                        openPorts[port] = 'https'
                    elif  service == 'https-proxy':
                        openPorts[port] = 'https'
                    else:
                        openPorts[port] = str(service)
                else:
                    print("Port ", port, " is ", portState)
            if not openPorts:
                print("Could not find any open ports for host at ", ip)
        else:
            print("Host at ip: ", ip, " is probably down. State is: ", hostState)
    return openPorts
