import Fetcher
import urllib.request
import urllib.parse


def checkLogin(URL, devType):
    if "nextUrl" in devType.keys():
        if devType['auth']['type'] == "form":
            keys = devType['auth']['credentials'].keys()
            newURL = URL+devType['nextUrl']+ "?"\
                     + list(keys)[0] + "=" + devType['auth']['credentials']['username']\
                     + list(keys)[1] + "=" + devType['auth']['credentials']['password']
            #print("new url:", newURL)
            response = Fetcher.fetch(newURL)
            #print(response)
            if type(response) is not int:
                status = response.getcode()
                if status == 200:
                    print("Device with url", URL, "still uses standard login credentials.")
                else:
                    print("Device with url", URL, "doesn't use standard login credentials.")
            else:
                # if get fails, try post
                details = urllib.parse.\
                    urlencode({'username': devType['auth']['credentials']['username'],
                                                  'password': devType['auth']['credentials']['password']})
                details = details.encode('UTF-8')
                newURL = URL + devType['nextUrl']
                url = urllib.request.Request(
                    newURL,
                    details)
                url.add_header("User-Agent",
                               "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13")

                try:
                    responseData = urllib.request.urlopen(url)
                    status = responseData.getcode()
                except urllib.request.HTTPError as e:
                    status = e.code
                if status == 200:
                    print("Device with url", URL, "still uses standard login credentials.")
                else:
                    print("Device with url", URL, "doesn't use standard login credentials.")
        elif devType['auth']['type'] == "basic":
            #copied from ... TODO: Quelle
            # create a password manager
            password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()

            # Add the username and password.
            # If we knew the realm, we could use it instead of None.
            top_level_url = URL+devType['nextUrl']
            username = devType['auth']['credentials']['username']
            password = devType['auth']['credentials']['password']
            password_mgr.add_password(None, top_level_url, username, password)

            handler = urllib.request.HTTPBasicAuthHandler(password_mgr)

            # create "opener" (OpenerDirector instance)
            opener = urllib.request.build_opener(handler)

            # use the opener to fetch a URL
            try:
                result = opener.open(top_level_url)

                # Install the opener.
                # Now all calls to urllib.request.urlopen use our opener.
                urllib.request.install_opener(opener)

                status = result.getcode()
                #print(result.getcode())
            except urllib.request.HTTPError as e:
                status = e.code
                #print(status)

            if status == 200:
                print("Device with url", URL, "still uses standard login credentials.")
            else:
                print("Device with url", URL, "doesn't use standard login credentials.")