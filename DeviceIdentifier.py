from bs4 import BeautifulSoup
import re
import sys

def searchForDevType(response, devices):
    html = str(response.read())
    soup = BeautifulSoup(html, 'lxml')
    if bool(devices):
        for device in devices["http"].keys():
            devTypePattern = devices["http"][device]['devTypePattern']
            if "head" in devTypePattern.keys():
                if devTypePattern['head']['tag'] == "title":
                    if devTypePattern['head']['pattern'][0] == "==":
                        if soup.title.string == devTypePattern['head']['pattern'][1]:
                            print("device found:", device)
                            return devices["http"][device]
                    elif devTypePattern['head']['pattern'][0] == "regex":
                        if re.match(devTypePattern['head']['pattern'][1], soup.title.string):
                            print("device found:", device)
                            return devices["http"][device]
                elif devTypePattern['head']['tag'] == "meta":
                    if devTypePattern['head']['pattern'][0] == "==":
                        for meta in soup.find_all('meta'):
                            if meta == devTypePattern['head']['pattern'][1]:
                                print("device found:", device)
                                return devices["http"][device]
                    elif devTypePattern['head']['pattern'][0] == "regex":
                        for meta in soup.find_all('meta'):
                            if re.match(devTypePattern['head']['pattern'][1], meta):
                                print("device found:", device)
                                return devices["http"][device]
            elif "body" in devTypePattern.keys():
                if devTypePattern['body']['tag'] != "":
                    for pattern in soup.find_all(devTypePattern['body']['tag']):
                        if re.match(devTypePattern['body']['pattern'][0], pattern):
                            print("device found:", device)
                            return devices["http"][device]
                else:
                    if re.match(devTypePattern['body']['pattern'][0], html):
                        print("device found:", device)
                        return devices["http"][device]

            elif "header" in devTypePattern.keys():
                print("Devtype requires matching header field.")
                # TODO: Check for matching header fields.
    else:
        print(devices)
        print("No devices.")
        sys.exit(2)
