"""
Functions to check devices, using http
"""

import re
import sys
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup

import HTTPHandler


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


def check_login(url, devtype):
    if "nextUrl" in devtype.keys():
        if devtype['auth']['type'] == "form":
            keys = devtype['auth']['credentials'].keys()
            new_url = url + devtype['nextUrl'] + "?" \
                      + list(keys)[0] + "=" + devtype['auth']['credentials']['username'] \
                      + list(keys)[1] + "=" + devtype['auth']['credentials']['password']
            # print("new url:", newURL)
            response = HTTPHandler.fetch(new_url)
            # print(response)
            if type(response) is not int:
                status = response.getcode()
                check_status(status, url)
            else:
                # if get fails, try post
                details = urllib.parse. \
                    urlencode({'username': devtype['auth']['credentials']['username'],
                               'password': devtype['auth']['credentials']['password']})
                details = details.encode('UTF-8')
                new_url = url + devtype['nextUrl']
                url = urllib.request.Request(
                    new_url,
                    details)
                url.add_header("User-Agent",
                               "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US)"
                               " AppleWebKit/525.13 (KHTML, like Gecko)"
                               " Chrome/0.2.149.29 Safari/525.13")

                try:
                    response_data = urllib.request.urlopen(url)
                    status = response_data.getcode()
                except urllib.request.HTTPError as e:
                    status = e.code
                check_status(status, url)
        elif devtype['auth']['type'] == "basic":
            password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
            top_level_url = url + devtype['nextUrl']
            username = devtype['auth']['credentials']['username']
            password = devtype['auth']['credentials']['password']
            password_mgr.add_password(None, top_level_url, username, password)

            handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
            opener = urllib.request.build_opener(handler)
            try:
                result = opener.open(top_level_url)
                urllib.request.install_opener(opener)
                status = result.getcode()
            except urllib.request.HTTPError as e:
                status = e.code
            check_status(status, url)


def check_status(status, url):
    if status == 200:
        print("Device with url", url, "still uses standard login credentials.")
    else:
        print("Device with url", url, "doesn't use standard login credentials.")
