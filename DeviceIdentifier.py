import re
import sys

from bs4 import BeautifulSoup


def search_for_devtype(response, devices):
    # TODO: Lambdas?
    html = str(response.read())
    soup = BeautifulSoup(html, 'lxml')
    if bool(devices):
        for device in devices["http"].keys():
            devtype_pattern = devices["http"][device]['devTypePattern']
            if "head" in devtype_pattern.keys():
                if devtype_pattern['head']['tag'] == "title":
                    if (devtype_pattern['head']['pattern'][0] == "==") \
                            and \
                            (soup.title.string == devtype_pattern['head']['pattern'][1]):
                        print("device found:", device)
                        return devices["http"][device]
                    elif devtype_pattern['head']['pattern'][0] == "regex" \
                            and \
                            re.match(devtype_pattern['head']['pattern'][1], soup.title.string):
                        print("device found:", device)
                        return devices["http"][device]
                elif devtype_pattern['head']['tag'] == "meta":
                    if devtype_pattern['head']['pattern'][0] == "==":
                        for meta in soup.find_all('meta'):
                            if meta == devtype_pattern['head']['pattern'][1]:
                                print("device found:", device)
                                return devices["http"][device]
                    elif devtype_pattern['head']['pattern'][0] == "regex":
                        for meta in soup.find_all('meta'):
                            if re.match(devtype_pattern['head']['pattern'][1], meta):
                                print("device found:", device)
                                return devices["http"][device]
            elif "body" in devtype_pattern.keys():
                if devtype_pattern['body']['tag'] != "":
                    for pattern in soup.find_all(devtype_pattern['body']['tag']):
                        if re.match(devtype_pattern['body']['pattern'][0], pattern):
                            print("device found:", device)
                            return devices["http"][device]
                else:
                    if re.match(devtype_pattern['body']['pattern'][0], html):
                        print("device found:", device)
                        return devices["http"][device]

            elif "header" in devtype_pattern.keys():
                print("Devtype requires matching header field.")
                # TODO: Check for matching header fields.
    else:
        print(devices)
        print("No devices.")
        sys.exit(2)
