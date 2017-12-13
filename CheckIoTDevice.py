import DeviceIdentifier
import Fetcher
import CheckLogin
import sshcheck


def check(ip, scanResults, devices):
    #TODO: Programm springt aus der Schleife, nach Überprüfung von HTTP;
    for port in scanResults.keys():
        print(port)
        if scanResults[port] == 'ssh':
            loginPossible = False
            for login in devices['ssh']:
                loginPossible = sshcheck.sshcheck(ip, port, devices['ssh'][login]['username'], devices['ssh'][login]['password'])
                if loginPossible:
                    break
            if not loginPossible :
                print("Could not log into ssh with any default password.")
        elif scanResults[port] == 'http':
            URL = composeURL(ip, port)
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
                else:
                    return CheckLogin.checkLogin(URL, devType)
            else:
                print("unexpected response: ", response)
        else:
            print("Could not check port", port, ", because the service is not supported. Service is:", scanResults[port])


def composeURL(ip, port):
    portStr = str(port)
    urlStr = "http://" + ip + ":" + portStr
    return urlStr