import iotscanner

class ResponseHandler():
    """
    Methods to handle html response.
    """

    PAGE_NOT_FOUND = 404
    UNAUTHORIZED = 401
    SUCCESSFUL = 200
    CONNECTION_REFUSED = 595

    def is_available(self, response):
        """
        Checking the response message, to see if the page is generally available.
        :param response: any
        :return: bool
        """
        if self.is_successful(response):
            return True
        elif response == self.UNAUTHORIZED:
            return True
        elif response == self.PAGE_NOT_FOUND:
            if iotscanner.VERBOSE:
                print("Got 404 response.")
            return False
        elif response == self.CONNECTION_REFUSED:
            if iotscanner.VERBOSE:
                print("Failed to establish TCP connection.")
            return False
        else:
            if iotscanner.VERBOSE:
                print("unexpected status code:", response)
            return False

    def is_successful(self, response):
        if type(response) is not int \
                and response.getcode() == self.SUCCESSFUL:
            return True
        else:
            return False


    def print_success_message(self, device_name, url):
        print("Device, identified as {0}, with url {1} still uses standard login credentials.".format(device_name, url))

    def print_failure_message(self, device_name, url):
        print("Device {0} with url {1} does not use standard login credentials.".format(
             device_name, url))