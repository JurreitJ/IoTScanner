import re
import netaddr

class IPHandler:
    def __init__(self):
        pass

    def getIPList(self, ipAddressesString):
        ipList = list()
        ipAddresses = re.split("[\,]", ipAddressesString)
        for ipAddress in ipAddresses:
            matchIPRange = re.search("[-]", ipAddress)
            if matchIPRange:
                start = ipAddress[:matchIPRange.start()]
                end = ipAddress[matchIPRange.end():]
                print(start, "|", end)
                for ipInt in range(self.ip2Int(start), self.ip2Int(end) + 1):
                    ipList.append(self.int2IP(ipInt))
            else:
                ipList.append(ipAddress)
        return ipList

    def ip2Int(self, ipAddress):
        return int(netaddr.IPAddress(ipAddress))

    def int2IP(self, ipInt):
        return str(netaddr.IPAddress(ipInt))