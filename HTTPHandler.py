"""
Functions to handle http requests and responses
"""

import urllib.request


def fetch(url):
    try:
        response = urllib.request.urlopen(url)
        print("Scanning", url, "...")
        return response
    except urllib.request.HTTPError as e:
        return e.code


def compose_url(ip, port):
    port_str = str(port)
    url_str = "http://" + ip + ":" + port_str
    return url_str
