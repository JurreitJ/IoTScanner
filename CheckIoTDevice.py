from DeviceIdentifier import DeviceIdentifier
from Fetcher import Fetcher
from CheckLogin import CheckLogin

class CheckIoTDevice:

    def __init__(self, devices):
        self.devices = devices


    def check(self, ip, scanResults):
        deviceIdentifier = DeviceIdentifier(self.devices)
        fetcher = Fetcher()
        checkLogin = CheckLogin()
        for port in scanResults.keys():
            if scanResults[port] == 'http':
                URL = self.composeURL(ip, port)
                numOfResults = -1
                results = list(dict())
                response = fetcher.fetch(URL)
                if type(response) is int:
                    if response == 401:
                        devType = deviceIdentifier.searchForDevType(response)
                        #return checkLogin.checkLogin(URL, devType)
                    elif response == 404:
                        print("cannot find dev type for ", URL, " due to 404 response." )
                    elif response == 595:
                        print("device ", URL, ": failed to establish TCP connection.")
                    else:
                        print("unexpected status code:", response)
                elif response.getcode() == 200:
                    devType = deviceIdentifier.searchForDevType(response)
                    if not devType:
                        print("No matching device found.")
                        exit(0)
                    else:
                        return checkLogin.checkLogin(URL, devType)
                else:
                    print("unexpected response: ", response)
            else:
                print("Could not check port", port, ", because no http service is running. Service is:", scanResults[port])
                #TODO: check other connections; e.g. HTTPS, FTP

    def composeURL(self, ip, port):
        portStr = str(port)
        urlStr = "http://" + ip + ":" + portStr
        return urlStr