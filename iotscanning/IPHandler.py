import re

import netaddr


def get_ip_list(ip_addresses_string):
    ip_list = list()
    ip_addresses = re.split("[,]", ip_addresses_string)
    for ipAddress in ip_addresses:
        match_ip_range = re.search("[-]", ipAddress)
        if match_ip_range:
            start = ipAddress[:match_ip_range.start()]
            end = ipAddress[match_ip_range.end():]
            print(start, "|", end)
            for ip_int in range(ip2int(start), ip2int(end) + 1):
                ip_list.append(int2ip(ip_int))
        else:
            ip_list.append(ipAddress)
    return ip_list


def ip2int(ip_address):
    return int(netaddr.IPAddress(ip_address))


def int2ip(ip_int):
    return str(netaddr.IPAddress(ip_int))
