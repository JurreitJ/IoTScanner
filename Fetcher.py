import urllib.request

class Fetcher:
    def __init__(self):
        pass

    def fetch(self, url):
        try:
            response = urllib.request.urlopen(url)
            print("Scanning", url, "...")
            return response
        except urllib.request.HTTPError as e:
            return e.code