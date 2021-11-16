#!/usr/bin/env python

import paramiko

ip = "192.168.41.114"
port = 22
user = "gberzins"
password = "Ekstragol No G0@l"


def ssh_login_check(ip, port, user, passwd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(ip, port=port, username=user, password=passwd)
        return True
    except paramiko.ssh_exception.AuthenticationException:
        return False
    print("Something happended")


valid = ssh_login_check(ip, port, user, password)
if valid:
    print("[✅] Login successful")
else:
    print("[❌] Login failed.")
