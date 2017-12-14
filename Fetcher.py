import urllib.request


def fetch(url):
    try:
        response = urllib.request.urlopen(url)
        print("Scanning", url, "...")
        return response
    except urllib.request.HTTPError as e:
        return e.code
