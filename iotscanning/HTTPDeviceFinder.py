from bs4 import BeautifulSoup

import iotscanning
from iotscanning.DeviceDataHandler import DeviceDataHandler
from iotscanning.PatternMatcher import PatternMatcher


class HTTPDeviceFinder:
    """
    Methods to identify the found device.
    """
    def __init__(self, url):
        self.url = url
        self.response = None
        self.devtype_pattern = None
        self.html_position = None
        self.tag_name = None
        self.operator = None
        self.pattern = None
        self.pattern_matcher = PatternMatcher()


    def search_for_device(self, response):
        """
        Searches html response for patterns, that match with patterns of the devices in the device data dictionary.
        :param response:
        :return: found device: str:
        """
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

    def check_body(self):
        """
        Check html body for matching patterns.
        Returns True, if a matching pattern is found.
        :return: bool
        """
        html = str(self.response.read())
        soup = BeautifulSoup(html, 'lxml')
        found_device = False
        if self.pattern_matcher.is_title(self.tag_name):
            if self.pattern_matcher.is_equals(self.operator):
                found_device = self.pattern_matcher.match_equals(soup.title.string, self.pattern)
            elif self.pattern_matcher.is_regex(self.operator):
                found_device = self.pattern_matcher.match_regex(soup.title.string, self.pattern)
        elif self.pattern_matcher.is_meta(self.tag_name):
            if self.pattern_matcher.is_equals(self.operator):
                for meta in soup.find_all('meta'):
                    if self.pattern_matcher.match_equals(meta, self.pattern):
                        found_device = True
                        break
            elif self.pattern_matcher.is_regex(self.operator):
                for meta in soup.find_all('meta'):
                    if self.pattern_matcher.match_regex(meta, self.pattern):
                        found_device = True
                        break
        elif not self.pattern_matcher.is_empty_tag(self.tag_name):
            for pattern in soup.find_all(self.tag_name):
                if self.pattern_matcher.match_regex(str(pattern), self.pattern):
                    found_device = True
                    break
        else:
            found_device = self.pattern_matcher.match_regex(html, self.pattern)
        return found_device


    def get_data(self, index):
        device_handler = DeviceDataHandler()
        device = iotscanning.DEVICES["http"][index]
        self.devtype_pattern = device_handler.retrieve_device_pattern(device)
        self.html_position = device_handler.retrieve_html_position(self.devtype_pattern)
        self.tag_name = device_handler.retrieve_tag(self.devtype_pattern, self.html_position)
        self.operator = device_handler.retrieve_comparison_operator(self.devtype_pattern,
                                                                             self.html_position)
        self.pattern = device_handler.retrieve_comparison_pattern(self.devtype_pattern,
                                                                           self.html_position)



