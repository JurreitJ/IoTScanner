import iotscanning
from iotscanning import HTTPFetcher
from iotscanning import DeviceDataHandler
from iotscanning.ResponseHandler import ResponseHandler
import urllib.response
import urllib.request


class LoginCheckHTTP():
    def __init__(self, device_name, url):
        self.device = iotscanning.DEVICES["http"][device_name]
        self.auth_type = DeviceDataHandler.retrieve_auth_type(self.device)
        self.credentials_keys = DeviceDataHandler.retrieve_credentials_keys(self.device)
        self.username = DeviceDataHandler.retrieve_username(self.device)
        self.password = DeviceDataHandler.retrieve_password(self.device)
        self.next_url = DeviceDataHandler.retrieve_next_url(self.device)
        self.url = url
        self.device_name = device_name
        self.response_handler = ResponseHandler()

    def check_login(self):
        if "nextUrl" in self.device.keys():
            if self.is_authtype_form():
                self.check_form_login()
            elif self.is_authtype_basic():
                self.check_basic_login()
        else:
            if iotscanning.VERBOSE:
                print("Checking login is not possible, due to missing information.")


    def check_form_login(self):
        new_url = self.url + self.next_url + "?" \
                  + list(self.credentials_keys)[0] + "=" + self.username \
                  + list(self.credentials_keys)[1] + "=" + self.password
        response = HTTPFetcher.fetch(new_url)
        if self.response_handler.is_successful(response):
            self.response_handler.print_success_message(self.device_name, self.url)
        else:
            # if get fails, try post
            new_url = self.url + self.next_url
            try:
                response = HTTPFetcher.fetch_via_post(new_url, self.username, self.password)
                if self.response_handler.is_successful(response):
                    self.response_handler.print_success_message(self.device_name, self.url)
            except urllib.request.HTTPError as e:
                self.response_handler.print_failure_message(self.device_name, self.url)


    def check_basic_login(self):
        password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        top_level_url = self.url + self.next_url
        password_mgr.add_password(None, top_level_url, self.username, self.password)

        handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
        opener = urllib.request.build_opener(handler)
        try:
            result = opener.open(top_level_url)
            urllib.request.install_opener(opener)
            if self.response_handler.is_successful(result):
                self.response_handler.print_success_message(self.device_name, self.url)
        except urllib.request.HTTPError as e:
            self.response_handler.print_failure_message(self.device_name, self.url)

    def is_authtype_form(self):
        if self.auth_type == "form":
            return True
        else:
            return False

    def is_authtype_basic(self):
        if self.auth_type == "basic":
            return True
        else:
            return False

