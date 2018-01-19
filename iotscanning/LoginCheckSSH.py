import paramiko

import iotscanning

class LoginCheckSSH():
    """
    Functions to check, whether an ssh connection can be established,
    using the given address and credentials
    """
    def login_check(self, host, port, username, password):
        """
        Check if login to ssh server is possible at the given host and port, using the username and password.
        Returns True, if login was successful.
        :param host: str
        :param port: int
        :param username: str
        :param password: str
        :return: bool
        """
        login_possible = False
        ssh = paramiko.SSHClient()
        # TODO: handle host keys; do not simply accept everyone
        ssh.set_missing_host_key_policy(
            paramiko.AutoAddPolicy())
        try:
            ssh.connect(host, port, username, password)
            login_possible = True
            print("SSH login with standard credentials, username: {0} and password: {1} is possible.".format(username,
                                                                                                               password))
        except Exception as e:
            if iotscanning.VERBOSE:
                print(e, "username: ", username, "password: ", password)
        ssh.close()
        return login_possible

    def bruteforce_ssh(self, host, port, wordlist):
        """
        Try logging into ssh server at given host and port by bruteforce with credentials from the given wordlist.
        :param host: str
        :param port: int
        :param wordlist:
        :return: bool
        """
        login_possible = False
        # Read wordlist from the path, given in the configuration file.
        file = open(wordlist["file"], "r")
        for line in file:
            username = line.split(":", 1)[0]
            temp_password = line.split(":", 1)[1]
            password = temp_password.split("\n", 1)[0]
            ssh = paramiko.SSHClient()
            # TODO: handle host keys; do not simply accept everyone
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                ssh.connect(host, port, username, password)
                login_possible = True
                print("SSH login with standard credentials, username: {0} and password: {1} is possible.".format(username, password))
                break
            except Exception as e:
                if iotscanning.VERBOSE:
                    print(e, "username: ", username, "password: ", password)
            ssh.close()
        return login_possible
