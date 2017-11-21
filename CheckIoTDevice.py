import DeviceIdentifier
import Fetcher
import CheckLogin


def check(ip, scanResults, devices):
    for port in scanResults.keys():
        if scanResults[port] == 'http':
            URL = composeURL(ip, port)
            numOfResults = -1
            results = list(dict())
            response = Fetcher.fetch(URL)
            if type(response) is int:
                if response == 401:
                    devType = DeviceIdentifier.searchForDevType(response, devices)
                    #return checkLogin.checkLogin(URL, devType)
                elif response == 404:
                    print("cannot find dev type for ", URL, " due to 404 response." )
                elif response == 595:
                    print("device ", URL, ": failed to establish TCP connection.")
                else:
                    print("unexpected status code:", response)
            elif response.getcode() == 200:
                devType = DeviceIdentifier.searchForDevType(response, devices)
                if not devType:
                    print("No matching device found.")
                    exit(0)
                else:
                    return CheckLogin.checkLogin(URL, devType)
            else:
                print("unexpected response: ", response)
        else:
            print("Could not check port", port, ", because no http service is running. Service is:", scanResults[port])
            #TODO: check other connections; e.g. HTTPS, FTP

def composeURL(ip, port):
    portStr = str(port)
    urlStr = "http://" + ip + ":" + portStr
    return urlStr