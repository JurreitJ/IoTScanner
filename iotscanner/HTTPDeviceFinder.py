from bs4 import BeautifulSoup

import iotscanner
from iotscanner.DeviceDataHandler import DeviceDataHandler
from iotscanner.PatternMatcher import PatternMatcher


class HTTPDeviceFinder:
    """
    Methods to identify the found device.
    """

    def __init__(self, response):
        self.devtype_pattern = None
        self.html_position = None
        self.tag_name = None
        self.operator = None
        self.pattern = None
        self.response = response
        self.pattern_matcher = PatternMatcher()
        self.html = self.read_response()
        self.soup = self.get_soup(self.html)


    def search_for_device(self):
        """
        Searches html response for patterns, that match with patterns of the devices in the device data dictionary.
        :param response:
        :return: found device: str:
        """
        device_found = None
        for device_name in iotscanner.DEVICES["http"].keys():
            self.get_data(device_name)
            if self.pattern_matcher.is_header(self.html_position) and self.header_matches():
                device_found = device_name
                break
            elif self.body_matches():
                device_found = device_name
                break
        if device_found is not None:
            print("Device found:", device_found)
            return device_found

    def header_matches(self):
        """
        Check header field for matching patterns.
        Returns True, if a matching pattern is found.
        :return: bool
        """
        headers = self.response.info()
        found_device = False
        for header in headers:
            if self.pattern_matcher.is_equals(self.operator) \
                    and self.pattern_matcher.match_equals(header[self.tag_name], self.pattern):
                found_device = True
                break
            elif self.pattern_matcher.is_regex(self.operator) \
                    and self.pattern_matcher.match_regex(header[self.tag_name], self.pattern):
                found_device = True
                break
        return found_device

    def body_matches(self):
        """
        Check html body for matching patterns.
        Returns True, if a matching pattern is found.
        :return: bool
        """
        found_device = False
        if self.pattern_matcher.is_title(self.tag_name):
            if self.pattern_matcher.is_equals(self.operator):
                found_device = self.pattern_matcher.match_equals(self.soup.title.string, self.pattern)
            elif self.pattern_matcher.is_regex(self.operator):
                found_device = self.pattern_matcher.match_regex(self.soup.title.string, self.pattern)
        elif self.pattern_matcher.is_meta(self.tag_name):
            if self.pattern_matcher.is_equals(self.operator):
                for meta in self.soup.find_all('meta'):
                    if self.pattern_matcher.match_equals(meta, self.pattern):
                        found_device = True
                        break
            elif self.pattern_matcher.is_regex(self.operator):
                for meta in self.soup.find_all('meta'):
                    if self.pattern_matcher.match_regex(meta, self.pattern):
                        found_device = True
                        break
        elif not self.pattern_matcher.is_empty_tag(self.tag_name):
            for pattern in self.soup.find_all(self.tag_name):
                if self.pattern_matcher.match_regex(str(pattern), self.pattern):
                    found_device = True
                    break
        else:
            found_device = self.pattern_matcher.match_regex(self.html, self.pattern)
        return found_device

    def get_data(self, index):
        device_handler = DeviceDataHandler()
        device = iotscanner.DEVICES["http"][index]
        self.devtype_pattern = device_handler.retrieve_device_pattern(device)
        self.html_position = device_handler.retrieve_html_position(self.devtype_pattern)
        self.tag_name = device_handler.retrieve_tag(self.devtype_pattern, self.html_position)
        self.operator = device_handler.retrieve_comparison_operator(self.devtype_pattern,
                                                                    self.html_position)
        self.pattern = device_handler.retrieve_comparison_pattern(self.devtype_pattern,
                                                                  self.html_position)

    def read_response(self):
        return str(self.response.read())

    def get_soup(self, html):
        return BeautifulSoup(html, 'lxml')