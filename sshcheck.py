import paramiko

def sshcheck(host, username, password, port = 22):
    ssh = paramiko.SSHClient()
    #TODO: handle host keys; do not simply accept everyone
    ssh.set_missing_host_key_policy(
    paramiko.AutoAddPolicy())

    try:
        ssh.connect(host, port, username, password)
    except Exception as e:
        print(e)

    ssh.close()