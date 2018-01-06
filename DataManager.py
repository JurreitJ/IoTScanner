"""
Functions to read device from json file and save important data
"""

import json
import sys


def read_devices(dev_config_input):
    try:
        with open(dev_config_input) as devConfigFile:
            return json.load(devConfigFile)
    except json.decoder.JSONDecodeError:
        print("Could not load devices.")
        sys.exit(2)


def retrieve_tag(device, position):
    return device[position]['tag']


def retrieve_device_pattern(device):
    return device['devTypePattern']


def retrieve_comparison_operator(device, position):
    return device[position]['pattern'][0]


def retrieve_comparison_pattern(device, position):
    return device[position]['pattern'][1]


def retrieve_html_position(device):
    if "head" in device.keys():
        return "head"
    elif "body" in device.keys():
        return "body"
    elif "header" in device.keys():
        return "header"
    else:
        return None


def retrieve_auth_type(device):
    return device['auth']['type']


def retrieve_username(device):
    return device['auth']['credentials']['username']


def retrieve_password(device):
    return device['auth']['credentials']['password']


def retrieve_credentials_keys(device):
    return device['auth']['credentials'].keys()


def retrieve_next_url(device):
    return device['nextUrl']


def retrieve_header_tag(device):
    return device['header']['tag']


def retrieve_header_pattern(device):
    return device['header']['pattern'][1]


def retrieve_header_comparison_operator(device):
    return device['header']['pattern'][0]
