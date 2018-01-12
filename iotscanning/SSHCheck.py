"""
Functions to check, whether an ssh connection can be established,
using the given address and credentials
"""

import paramiko
import iotscanning


def ssh_check(host, port, username, password):
    login_possible = False
    ssh = paramiko.SSHClient()
    # TODO: handle host keys; do not simply accept everyone
    ssh.set_missing_host_key_policy(
        paramiko.AutoAddPolicy())

    try:
        ssh.connect(host, port, username, password)
        login_possible = True
        print("SSH login with standard credentials, username:", username, ", password:", password, "is possible.")
    except Exception as e:
        if iotscanning.verbose:
            print(e, "username: ", username, "password: ", password)
    ssh.close()
    return login_possible

def bruteforce_ssh(host, port, wordlist):
    login_possible = False
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
            print("SSH login with standard credentials, username:", username, ", password:", password, "is possible.")
            break
        except Exception as e:
            if iotscanning.verbose:
                print(e, "username: ", username, "password: ", password)
        ssh.close()
    return login_possible
