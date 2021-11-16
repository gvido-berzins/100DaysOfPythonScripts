import impacket
from impacket.smbconnection import SMBConnection

ip = "0.0.0.0"
server = ip
username = "cny"
password = "cn"

try:
    smb = SMBConnection(server, ip)
    smb.login(username, password)
    print("Success")
except impacket.smbconnection.SessionError:
    print("Could not authenticate user")
