from bs4 import BeautifulSoup
import re
import sys

class DeviceIdentifier:

    def __init__(self, devices):
        self.devices = devices

    def searchForDevType(self, response):
        html = str(response.read())
        soup = BeautifulSoup(html, 'lxml')
        if bool(self.devices):
            for device in self.devices["http"].keys():
                devTypePattern = self.devices["http"][device]['devTypePattern']
                if "head" in devTypePattern.keys():
                    if devTypePattern['head']['tag'] == "title":
                        if devTypePattern['head']['pattern'][0] == "==":
                            if soup.title.string == devTypePattern['head']['pattern'][1]:
                                print("device found:", device)
                                return self.devices["http"][device]
                        elif devTypePattern['head']['pattern'][0] == "regex":
                            if re.match(devTypePattern['head']['pattern'][1], soup.title.string):
                                print("device found:", device)
                                return self.devices["http"][device]
                    elif devTypePattern['head']['tag'] == "meta":
                        if devTypePattern['head']['pattern'][0] == "==":
                            for meta in soup.find_all('meta'):
                                if meta == devTypePattern['head']['pattern'][1]:
                                    print("device found:", device)
                                    return self.devices["http"][device]
                        elif devTypePattern['head']['pattern'][0] == "regex":
                            for meta in soup.find_all('meta'):
                                if re.match(devTypePattern['head']['pattern'][1], meta):
                                    print("device found:", device)
                                    return self.devices["http"][device]
                elif "body" in devTypePattern.keys():
                    if devTypePattern['body']['tag'] != "":
                        for pattern in soup.find_all(devTypePattern['body']['tag']):
                            if re.match(devTypePattern['body']['pattern'][0], pattern):
                                print("device found:", device)
                                return self.devices["http"][device]
                    else:
                        if re.match(devTypePattern['body']['pattern'][0], html):
                            print("device found:", device)
                            return self.devices["http"][device]

                elif "header" in devTypePattern.keys():
                    print("Devtype requires matching header field.")
                    # TODO: Check for matching header fields.
        else:
            print(self.devices)
            print("No devices.")
            sys.exit(2)
