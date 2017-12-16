"""
Functions to check devices, using http
"""

import re
import sys
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup

import DataManager
import HTTPHandler


class HTTPCheck:
    __devtype_pattern = None
    __tag_name = None
    __comparison_pattern = None
    __comparison_operator = None
    __html_position = None
    __auth_type = None
    __username = None
    __password = None
    __credentials_keys = None
    __next_url = None

    def __init__(self, devices, url):
        self.devices = devices
        self.url = url

    def search_for_devtype(self, response):
        # TODO: Lambdas?
        html = str(response.read())
        soup = BeautifulSoup(html, 'lxml')
        if bool(self.devices):
            for device in self.devices["http"].keys():
                self.get_data(device)
                self.__html_position = DataManager.retrieve_html_position(device)
                if self.__html_position == "header":
                    pass
                    # TODO: Match header fields
                else:
                    if self.__tag_name == "title":
                        if (self.__comparison_operator == "==") \
                                and \
                                (soup.title.string == self.__comparison_pattern):
                            print("device found:", device)
                            return self.devices["http"][device]
                        elif self.__comparison_operator == "regex" \
                                and \
                                re.match(self.__comparison_pattern, soup.title.string):
                            print("device found:", device)
                            return self.devices["http"][device]
                    elif self.__tag_name == "meta":
                        if self.__comparison_operator == "==":
                            for meta in soup.find_all('meta'):
                                if meta == self.__comparison_pattern:
                                    print("device found:", device)
                                    return self.devices["http"][device]
                        elif self.__comparison_operator == "regex":
                            for meta in soup.find_all('meta'):
                                if re.match(self.__comparison_pattern, meta):
                                    print("device found:", device)
                                    return self.devices["http"][device]
                    if self.__tag_name != "":
                        for pattern in soup.find_all(self.__tag_name):
                            if re.match(self.__comparison_pattern, pattern):
                                print("device found:", device)
                                return self.devices["http"][device]
                    else:
                        if re.match(self.__comparison_pattern, html):
                            print("device found:", device)
                            return self.devices["http"][device]
        else:
            print(self.devices)
            print("No devices.")
            sys.exit(2)

    def check_login(self, devtype):
        if "nextUrl" in devtype.keys():
            if self.__auth_type == "form":
                new_url = self.url + self.__next_url + "?" \
                          + list(self.__credentials_keys)[0] + "=" + self.__username \
                          + list(self.__credentials_keys)[1] + "=" + self.__password
                # print("new url:", newURL)
                response = HTTPHandler.fetch(new_url)
                # print(response)
                if type(response) is not int:
                    status = response.getcode()
                    self.check_status(status)
                else:
                    # if get fails, try post
                    details = urllib.parse. \
                        urlencode({'username': self.__username,
                                   'password': self.__password})
                    details = details.encode('UTF-8')
                    new_url = self.url + self.__next_url
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
                    self.check_status(status)
            elif self.__auth_type == "basic":
                password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
                top_level_url = self.url + self.__next_url
                username = self.__username
                password = self.__password
                password_mgr.add_password(None, top_level_url, username, password)

                handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
                opener = urllib.request.build_opener(handler)
                try:
                    result = opener.open(top_level_url)
                    urllib.request.install_opener(opener)
                    status = result.getcode()
                except urllib.request.HTTPError as e:
                    status = e.code
                self.check_status(status)

    def check_status(self, status):
        if status == 200:
            print("Device with url", self.url, "still uses standard login credentials.")
        else:
            print("Device with url", self.url, "doesn't use standard login credentials.")

    @staticmethod
    def check_availability(response):
        if type(response) is int:
            if response == 401:
                return True
            elif response == 404:
                print("Got 404 response.")
                return False
            elif response == 595:
                print("Failed to establish TCP connection.")
                return False
            else:
                print("unexpected status code:", response)
                return False
        elif response.getcode() == 200:
            return True
        else:
            print("unexpected response: ", response)
            return False

    def get_data(self, device):
        self.__devtype_pattern = DataManager.retrieve_device_pattern(self.devices, device)
        self.__tag_name = DataManager.retrieve_tag(self.__devtype_pattern, self.__html_position)
        self.__comparison_operator = DataManager.retrieve_comparison_operator(self.__devtype_pattern,
                                                                              self.__html_position)
        self.__auth_type = DataManager.retrieve_auth_type(device)
        self.__credentials_keys = DataManager.retrieve_credentials_keys(device)
        self.__username = DataManager.retrieve_username(device)
        self.__password = DataManager.retrieve_password(device)
        self.__next_url = DataManager.retrieve_next_url(device)
