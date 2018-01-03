"""
File to test new functionalities, before implementing;
Not Unit tests;
"""

import urllib.request

response = urllib.request.urlopen("https://www.google.de")
response = response.info()
print(response['server'])
