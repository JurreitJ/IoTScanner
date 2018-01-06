"""
Functions to handle http requests and responses
"""

import urllib.parse
import urllib.request


def fetch(url):
    try:
        response = urllib.request.urlopen(url)
        print("Scanning", url, "...")
        return response
    except urllib.request.HTTPError as e:
        return e.code


def fetch_via_post(url_to_fetch, username, password):
    details = urllib.parse. \
        urlencode({'username': username,
                   'password': password})
    details = details.encode('UTF-8')
    url = urllib.request.Request(
        url_to_fetch,
        details)
    url.add_header("User-Agent",
                   "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US)"
                   " AppleWebKit/525.13 (KHTML, like Gecko)"
                   " Chrome/0.2.149.29 Safari/525.13")

    try:
        response_data = urllib.request.urlopen(url)
        status = response_data.getcode()
        return status
    except urllib.request.HTTPError as e:
        status = e.code
        return status


def compose_url(ip, port):
    port_str = str(port)
    url_str = "http://" + ip + ":" + port_str
    return url_str
