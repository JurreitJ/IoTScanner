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

# TODO: Add functions to save device, url, username, etc.
