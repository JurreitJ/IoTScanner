import urllib.request
import urllib.request

import paramiko.client


def main():
    getHTML()

    client = paramiko.client.SSHClient()
    # client.connect("test.de", 22, "test", "test")


def getHTML():
    URL = "http://127.0.0.1:80/loginpost.php"
    html = fetch(URL)
    print(html)
    # soup = BeautifulSoup(html, 'lxml')
    # print(soup.prettify())


def fetch(url):
    details = urllib.parse. \
        urlencode({'username': "admin",
                   'password': "admin"})
    details = details.encode('UTF-8')
    print("details", details)
    url = urllib.request.Request(
        url,
        details)
    print("url", url)
    url.add_header("User-Agent",
                   "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13")

    try:
        responseData = urllib.request.urlopen(url)
        status = responseData.getcode()
        print("success")
    except urllib.request.HTTPError as e:
        status = e.code
    print(status)


if __name__ == '__main__':
    main()
