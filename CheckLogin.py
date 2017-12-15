import urllib.parse
import urllib.request

import Fetcher


def check_login(url, devtype):
    if "nextUrl" in devtype.keys():
        if devtype['auth']['type'] == "form":
            keys = devtype['auth']['credentials'].keys()
            new_url = url + devtype['nextUrl'] + "?" \
                      + list(keys)[0] + "=" + devtype['auth']['credentials']['username'] \
                      + list(keys)[1] + "=" + devtype['auth']['credentials']['password']
            # print("new url:", newURL)
            response = Fetcher.fetch(new_url)
            # print(response)
            if type(response) is not int:
                status = response.getcode()
                check_status(status, url)
            else:
                # if get fails, try post
                details = urllib.parse. \
                    urlencode({'username': devtype['auth']['credentials']['username'],
                               'password': devtype['auth']['credentials']['password']})
                details = details.encode('UTF-8')
                new_url = url + devtype['nextUrl']
                url = urllib.request.Request(
                    new_url,
                    details)
                url.add_header("User-Agent",
                               "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US)"
                               " AppleWebKit/525.13 (KHTML, like Gecko)"
                               " Chrome/0.2.149.29 Safari/525.13")

                try:
                    response_data = urllib.request.urlopen(url)
                    status = response_data.getcode()
                except urllib.request.HTTPError as e:
                    status = e.code
                check_status(status, url)
        elif devtype['auth']['type'] == "basic":
            password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
            top_level_url = url + devtype['nextUrl']
            username = devtype['auth']['credentials']['username']
            password = devtype['auth']['credentials']['password']
            password_mgr.add_password(None, top_level_url, username, password)

            handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
            opener = urllib.request.build_opener(handler)
            try:
                result = opener.open(top_level_url)
                urllib.request.install_opener(opener)
                status = result.getcode()
            except urllib.request.HTTPError as e:
                status = e.code
            check_status(status, url)


def check_status(status, url):
    if status == 200:
        print("Device with url", url, "still uses standard login credentials.")
    else:
        print("Device with url", url, "doesn't use standard login credentials.")
