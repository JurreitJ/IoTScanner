"""
Functions to check devices, using http
"""

import re
import sys
import urllib.request

from iotscanning import HTTPHandler
import iotscanning
from bs4 import BeautifulSoup

from iotscanning import DataManager


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
    __header_tag = None
    __header_pattern = None
    __header_comparison_operator = None

    def __init__(self, devices, url):
        self.devices = devices
        self.url = url
        self.device_found = None

    def search_for_devtype(self, response):
        html = str(response.read())
        headers = response.info()
        soup = BeautifulSoup(html, 'lxml')
        if bool(self.devices):
            for device in self.devices["http"].keys():
                self.get_data(device)
                if self.__html_position == "header":
                    self.__header_tag = DataManager.retrieve_header_tag(self.__devtype_pattern)
                    self.__header_comparison_operator = DataManager.retrieve_header_comparison_operator(
                        self.__devtype_pattern)
                    self.__header_pattern = DataManager.retrieve_header_pattern(self.__devtype_pattern)
                    for header in headers:
                        if self.__header_comparison_operator == "==" \
                                and \
                                        header[self.__header_tag] == self.__header_pattern:
                            self.device_found = device
                        elif self.__header_comparison_operator == "regex" \
                                and \
                                re.match(self.__header_pattern, header[self.__header_tag]):
                            self.device_found = device
                else:
                    if self.__tag_name == "title":
                        if (self.__comparison_operator == "==") \
                                and \
                                (soup.title.string == self.__comparison_pattern):
                            self.device_found = device
                        elif self.__comparison_operator == "regex" \
                                and \
                                re.match(self.__comparison_pattern, soup.title.string):
                            self.device_found = device
                    elif self.__tag_name == "meta":
                        if self.__comparison_operator == "==":
                            for meta in soup.find_all('meta'):
                                if meta == self.__comparison_pattern:
                                    self.device_found = device
                        elif self.__comparison_operator == "regex":
                            for meta in soup.find_all('meta'):
                                if re.match(self.__comparison_pattern, meta):
                                    self.device_found = device
                    elif self.__tag_name != "" and self.__tag_name != None:
                        for pattern in soup.find_all(self.__tag_name):
                            if re.match(self.__comparison_pattern, str(pattern)):
                                self.device_found = device
                    else:
                        if re.match(self.__comparison_pattern, html):
                            self.device_found = device
            if self.device_found is not None:
                if iotscanning.verbose:
                    print("Device found:", self.device_found)
                return self.devices["http"][self.device_found]
        else:
            print("No devices.")
            sys.exit(1)

    def check_login(self, devtype):
        if "nextUrl" in devtype.keys():
            if self.__auth_type == "form":
                new_url = self.url + self.__next_url + "?" \
                          + list(self.__credentials_keys)[0] + "=" + self.__username \
                          + list(self.__credentials_keys)[1] + "=" + self.__password
                response = HTTPHandler.fetch(new_url)
                if type(response) is not int:
                    status = response.getcode()
                    self.check_status(status)
                else:
                    # if get fails, try post
                    new_url = self.url + self.__next_url
                    status = HTTPHandler.fetch_via_post(new_url, self.__username, self.__password)
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
            print("Device, identified as {0}, with url {1} still uses standard login credentials.".format(self.device_found,
                  self.url))
        else:
            print("Device {0} with url {1} doesn't use standard login credentials.".format(self.device_found, self.url))

    @staticmethod
    def check_availability(response):
        if type(response) is int:
            if response == 401:
                return True
            elif response == 404:
                if iotscanning.verbose:
                    print("Got 404 response.")
                return False
            elif response == 595:
                if iotscanning.verbose:
                    print("Failed to establish TCP connection.")
                return False
            else:
                if iotscanning.verbose:
                    print("unexpected status code:", response)
                return False
        elif response.getcode() == 200:
            return True
        else:
            if iotscanning.verbose:
                print("unexpected response: ", response)
            return False

    def get_data(self, index):
        device = self.devices["http"][index]
        self.__devtype_pattern = DataManager.retrieve_device_pattern(device)
        self.__html_position = DataManager.retrieve_html_position(self.__devtype_pattern)
        self.__tag_name = DataManager.retrieve_tag(self.__devtype_pattern, self.__html_position)
        self.__comparison_operator = DataManager.retrieve_comparison_operator(self.__devtype_pattern,
                                                                              self.__html_position)
        self.__comparison_pattern = DataManager.retrieve_comparison_pattern(self.__devtype_pattern,
                                                                            self.__html_position)
        self.__auth_type = DataManager.retrieve_auth_type(device)
        self.__credentials_keys = DataManager.retrieve_credentials_keys(device)
        self.__username = DataManager.retrieve_username(device)
        self.__password = DataManager.retrieve_password(device)
        self.__next_url = DataManager.retrieve_next_url(device)
