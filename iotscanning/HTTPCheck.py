"""
Functions to check devices, using http
"""

import re
import sys
import urllib.request

from bs4 import BeautifulSoup

import iotscanning
from iotscanning import DeviceDataHandler
from iotscanning import HTTPFetcher


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


    def __init__(self, url):
        self.url = url
        self.response = None

    def search_for_device(self, response):
        self.response = response
        device_found = None
        for self.device in iotscanning.DEVICES["http"].keys():
            self.get_data(self.device)
            if self.is_header_field() and self.check_header():
                device_found = self.device
                break
            elif self.check_body():
                device_found = self.device
                break
        if device_found is not None:
            if iotscanning.VERBOSE:
                print("Device found:", device_found)
            return device_found


    def check_header(self):
        headers = self.response.info()
        tag = DeviceDataHandler.retrieve_header_tag(self.__devtype_pattern)
        comparison_operator = DeviceDataHandler.retrieve_header_comparison_operator(
            self.__devtype_pattern)
        pattern = DeviceDataHandler.retrieve_header_pattern(self.__devtype_pattern)
        found_device = False
        for header in headers:
            if self.is_equals(comparison_operator) \
                and self.match_equals(header[tag], pattern):
               found_device = True
               break
            elif self.is_regex(comparison_operator) \
                    and self.match_regex(header[tag], pattern):
                found_device = True
                break
        return found_device

    def check_body(self):
        tag_name = DeviceDataHandler.retrieve_tag(self.__devtype_pattern, self.__html_position)
        comparison_operator = DeviceDataHandler.retrieve_comparison_operator(self.__devtype_pattern,
                                                                                    self.__html_position)
        comparison_pattern = DeviceDataHandler.retrieve_comparison_pattern(self.__devtype_pattern,
                                                                                  self.__html_position)
        html = str(self.response.read())
        soup = BeautifulSoup(html, 'lxml')
        found_device = False
        if self.is_title(tag_name):
            if self.is_equals(comparison_operator):
                found_device = self.match_equals(soup.title.string, comparison_pattern)
            elif self.is_regex(comparison_operator):
                found_device = self.match_regex(soup.title.string, comparison_pattern)
        elif self.is_meta(tag_name):
            if self.is_equals(comparison_operator):
                for meta in soup.find_all('meta'):
                    if self.match_equals(meta, comparison_pattern):
                        found_device = True
                        break
            elif self.is_regex(comparison_operator):
                for meta in soup.find_all('meta'):
                    if self.match_regex(meta, comparison_pattern):
                        found_device = True
                        break
        elif not self.is_empty_tag(tag_name):
            for pattern in soup.find_all(self.__tag_name):
                if self.match_regex(str(pattern), comparison_pattern):
                    found_device = True
                    break
        else:
            found_device = self.match_regex(html, comparison_pattern)
        return found_device



    def check_login(self, device):
        if "nextUrl" in iotscanning.DEVICES['http'][device].keys():
            if self.is_authtype_form():
                self.check_form_login()
            elif self.is_authtype_basic():
                self.check_basic_login()

    def check_form_login(self):
        new_url = self.url + self.__next_url + "?" \
                  + list(self.__credentials_keys)[0] + "=" + self.__username \
                  + list(self.__credentials_keys)[1] + "=" + self.__password
        response = HTTPFetcher.fetch(new_url)
        if self.is_successful(response):
            self.print_success_message()
        else:
            # if get fails, try post
            new_url = self.url + self.__next_url
            try:
               response = HTTPFetcher.fetch_via_post(new_url, self.__username, self.__password)
               if self.is_successful(response):
                    self.print_success_message()
            except urllib.request.HTTPError as e:
                self.print_failure_message()

    def check_basic_login(self):
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
            if self.is_successful(result):
                self.print_success_message()
        except urllib.request.HTTPError as e:
            self.print_failure_message()


    def get_data(self, index):
        # TODO: Function needed?
        device = iotscanning.DEVICES["http"][index]
        self.__devtype_pattern = DeviceDataHandler.retrieve_device_pattern(device)
        self.__html_position = DeviceDataHandler.retrieve_html_position(self.__devtype_pattern)
        self.__auth_type = DeviceDataHandler.retrieve_auth_type(device)
        self.__credentials_keys = DeviceDataHandler.retrieve_credentials_keys(device)
        self.__username = DeviceDataHandler.retrieve_username(device)
        self.__password = DeviceDataHandler.retrieve_password(device)
        self.__next_url = DeviceDataHandler.retrieve_next_url(device)

    def is_header_field(self):
        if self.__html_position == "header":
            return True
        else:
            return False


    def is_authtype_form(self):
        if self.__auth_type == "form":
            return True
        else:
            return False



    def is_successful(self, response):
        if type(response) is not int\
                and response.getcode() == 200:
                return True
        else:
            return False

    def is_authtype_basic(self):
        if self.__auth_type == "basic":
            return True
        else:
            return False


    def is_regex(self, operator):
        if operator == "regex":
            return True
        else:
            return False

    def is_equals(self, operator):
        if operator == "==":
            return True
        else:
            return False

    def is_title(self, tag_name):
        if tag_name == "title":
            return True
        else:
            return False

    def is_meta(self, tag_name):
        if tag_name == "meta":
            return True
        else:
            return False

    def match_equals(self, string, pattern):
        if string == pattern:
            return True
        else:
            return False

    def match_regex(self, string, pattern):
        if re.match(pattern, string):
            return True
        else:
            return False

    def is_empty_tag(self, tag_name):
        if tag_name == "" and tag_name is None:
            return True
        else:
            return False

    def print_success_message(self):
        print("Device, identified as {0}, with url {1} still uses standard login credentials.".format(self.device,
                                                                                                      self.url))

    def print_failure_message(self):
        print("Device {0} with url {1} does not use standard login credentials.".format(
            self.device,
            self.url))


    def check_availability(self, response):
        if self.is_successful(response):
            return True
        elif response == 401:
            return True
        elif response == 404:
            if iotscanning.VERBOSE:
                print("Got 404 response.")
            return False
        elif response == 595:
            if iotscanning.VERBOSE:
                print("Failed to establish TCP connection.")
            return False
        else:
            if iotscanning.VERBOSE:
                print("unexpected status code:", response)
            return False
