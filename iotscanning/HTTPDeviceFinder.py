"""
Functions to check devices, using http
"""

from bs4 import BeautifulSoup

import iotscanning
from iotscanning import DeviceDataHandler
from iotscanning.PatternMatcher import PatternMatcher


class HTTPDeviceFinder:
    def __init__(self, url):
        self.url = url
        self.response = None
        self.devtype_pattern = None
        self.html_position = None
        self.pattern_matcher = PatternMatcher()


    def search_for_device(self, response):
        self.response = response
        device_found = None
        for self.device_name in iotscanning.DEVICES["http"].keys():
            self.get_data(self.device_name)
            if self.pattern_matcher.is_header(self.html_position) and self.check_header():
                device_found = self.device_name
                break
            elif self.check_body():
                device_found = self.device_name
                break
        if device_found is not None:
            if iotscanning.VERBOSE:
                print("Device found:", device_found)
            return device_found

    def check_header(self):
        headers = self.response.info()
        tag = DeviceDataHandler.retrieve_header_tag(self.devtype_pattern)
        comparison_operator = DeviceDataHandler.retrieve_header_comparison_operator(
            self.devtype_pattern)
        pattern = DeviceDataHandler.retrieve_header_pattern(self.devtype_pattern)
        found_device = False
        for header in headers:
            if self.pattern_matcher.is_equals(comparison_operator) \
                    and self.pattern_matcher.match_equals(header[tag], pattern):
                found_device = True
                break
            elif self.pattern_matcher.is_regex(comparison_operator) \
                    and self.pattern_matcher.match_regex(header[tag], pattern):
                found_device = True
                break
        return found_device

    def check_body(self):
        tag_name = DeviceDataHandler.retrieve_tag(self.devtype_pattern, self.html_position)
        comparison_operator = DeviceDataHandler.retrieve_comparison_operator(self.devtype_pattern,
                                                                             self.html_position)
        comparison_pattern = DeviceDataHandler.retrieve_comparison_pattern(self.devtype_pattern,
                                                                           self.html_position)
        html = str(self.response.read())
        soup = BeautifulSoup(html, 'lxml')
        found_device = False
        if self.pattern_matcher.is_title(tag_name):
            if self.pattern_matcher.is_equals(comparison_operator):
                found_device = self.pattern_matcher.match_equals(soup.title.string, comparison_pattern)
            elif self.pattern_matcher.is_regex(comparison_operator):
                found_device = self.pattern_matcher.match_regex(soup.title.string, comparison_pattern)
        elif self.pattern_matcher.is_meta(tag_name):
            if self.pattern_matcher.is_equals(comparison_operator):
                for meta in soup.find_all('meta'):
                    if self.pattern_matcher.match_equals(meta, comparison_pattern):
                        found_device = True
                        break
            elif self.pattern_matcher.is_regex(comparison_operator):
                for meta in soup.find_all('meta'):
                    if self.pattern_matcher.match_regex(meta, comparison_pattern):
                        found_device = True
                        break
        elif not self.pattern_matcher.is_empty_tag(tag_name):
            for pattern in soup.find_all(tag_name):
                if self.pattern_matcher.match_regex(str(pattern), comparison_pattern):
                    found_device = True
                    break
        else:
            found_device = self.pattern_matcher.match_regex(html, comparison_pattern)
        return found_device


    def get_data(self, index):
        device = iotscanning.DEVICES["http"][index]
        self.devtype_pattern = DeviceDataHandler.retrieve_device_pattern(device)
        self.html_position = DeviceDataHandler.retrieve_html_position(self.devtype_pattern)




