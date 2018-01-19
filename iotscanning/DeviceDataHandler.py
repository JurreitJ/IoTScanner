import json
import sys

class DeviceDataHandler():
    """
    Methods to retrieve device data from data dictionary.
    """
    def read_devices(self, dev_config_input):
        try:
            with open(dev_config_input) as devConfigFile:
                return json.load(devConfigFile)
        except json.decoder.JSONDecodeError:
            print("Could not load devices.")
            sys.exit(1)


    def retrieve_tag(self, device, position):
        return device[position]['tag']


    def retrieve_device_pattern(self, device):
        return device['devTypePattern']


    def retrieve_comparison_operator(self, device, position):
        return device[position]['pattern'][0]


    def retrieve_comparison_pattern(self, device, position):
        return device[position]['pattern'][1]


    def retrieve_html_position(self, device):
        """
        Searches for tagnames in device data and
        returns the html tag of the device.
        :param device:
        :return: str
        """
        if "head" in device.keys():
            return "head"
        elif "body" in device.keys():
            return "body"
        elif "header" in device.keys():
            return "header"
        else:
            return None


    def retrieve_auth_type(self, device):
        return device['auth']['type']


    def retrieve_username(self, device):
        return device['auth']['credentials']['username']


    def retrieve_password(self, device):
        return device['auth']['credentials']['password']


    def retrieve_credentials_keys(self, device):
        return device['auth']['credentials'].keys()


    def retrieve_next_url(self, device):
        return device['next_url']
