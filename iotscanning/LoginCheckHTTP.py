import iotscanning
from iotscanning import HTTPFetcher
from iotscanning.DeviceDataHandler import DeviceDataHandler
from iotscanning.ResponseHandler import ResponseHandler
import urllib.response
import urllib.request


class LoginCheckHTTP():
    """
    Methods to check, logging into the device with  HTTP login methods.
    """
    def __init__(self, device_name, url):
        self.device = iotscanning.DEVICES["http"][device_name]
        device_handler = DeviceDataHandler()
        self.auth_type = device_handler.retrieve_auth_type(self.device)
        self.credentials_keys = device_handler.retrieve_credentials_keys(self.device)
        self.username = device_handler.retrieve_username(self.device)
        self.password = device_handler.retrieve_password(self.device)
        self.next_url = device_handler.retrieve_next_url(self.device)
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
        """
        Check form login with the given device data.
        :return: None
        """
        # Compose url out of standard url (ip address + port), the provided url of the login page, and username and
        # password.
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
        """
        Check basic login with the given device data.
        :return: None
        """
        password_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        top_level_url = self.url + self.next_url
        password_manager.add_password(None, top_level_url, self.username, self.password)

        basic_auth_handler = urllib.request.HTTPBasicAuthHandler(password_manager)
        opener = urllib.request.build_opener(basic_auth_handler)
        try:
            result = opener.open(top_level_url)
            urllib.request.install_opener(opener)
            if self.response_handler.is_successful(result):
                self.response_handler.print_success_message(self.device_name, self.url)
        except urllib.request.HTTPError as e:
            # If an error occured, login was not successful.
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

