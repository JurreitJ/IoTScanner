import paramiko


def ssh_check(host, port, username, password):
    login_possible = False
    ssh = paramiko.SSHClient()
    # TODO: handle host keys; do not simply accept everyone
    ssh.set_missing_host_key_policy(
        paramiko.AutoAddPolicy())

    try:
        ssh.connect(host, port, username, password)
        login_possible = True
        print("SSH login with standard password", password)
    except Exception as e:
        print(e)
    ssh.close()
    return login_possible
