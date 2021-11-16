#!/usr/bin/env python

import argparse
import socket
from enum import Enum

import impacket
import paramiko
from impacket.smbconnection import SMBConnection

EMOJI_MAP = {
    "1": "1️⃣",
    "2": "2️⃣",
    "3": "3️⃣",
    "4": "4️⃣",
    "5": "5️⃣",
    "6": "6️⃣",
    "7": "7️⃣",
    "8": "8️⃣",
    "9": "9️⃣",
    "0": "0️⃣",
}


class Services(Enum):
    """Class representing the services and their ports"""

    FTP = 21
    SSH = 22
    # SFTP = 23
    SMB = 445
    # RDP = 3389


def recv(client_socket: socket.socket) -> str:
    """Receive data from a raw socket"""
    recv_len = 1
    recv_data = ""

    while recv_len:
        recv_buf = 4096
        data = client_socket.recv(recv_buf).decode()
        recv_len = len(data)
        recv_data += data

        if recv_len < recv_buf:
            break

    # print(f"📩 {recv_data}")
    return recv_data


def send(client_socket: socket.socket, buffer: str) -> None:
    """Send data to a connection"""
    client_socket.sendall(buffer.encode())
    # print(f"📤 {buffer}")


def login_ftp(
    client_socket: socket.socket, username: str, password: str
) -> bool:
    """Login into an FTP server and return the result"""
    user_cmd = f"USER {username}\r\n"
    pass_cmd = f"PASS {password}\r\n"
    recv(client_socket)
    send(client_socket, user_cmd)
    recv(client_socket)
    send(client_socket, pass_cmd)
    login_status = recv(client_socket)
    if "230" in login_status:
        return True
    return False


def connect(client_socket: socket.socket, ip: str, port: int) -> None:
    """Create a raw socket connection"""
    client_socket.connect((ip, port))


def login_ssh(ip: str, port: int, user: str, password: str):
    """Authenticate to the SSH server with paramiko client"""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=password)


def stuff_ssh(ip: str, port: int, username: str, password: str):
    """Perform stuffing on SSH"""
    status = False
    try:
        status = login_ssh(ip, port, username, password)
    except paramiko.ssh_exception.AuthenticationException:
        print("❗ Authentication failed.")
    except paramiko.ssh_exception.NoValidConnectionsError:
        print("❗ No valid connection.")

    pretty_status(ip, port, username, password, status)


def stuff_ftp(ip: str, port: int, username: str, password: str) -> bool:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    status = False

    try:
        connect(client_socket, ip, port)
        status = login_ftp(client_socket, username, password)
    except KeyboardInterrupt:
        print("⌨ Exiting, interrupted.")

    except ConnectionRefusedError:
        print("⁉️  Connection refused.")

    except socket.gaierror:
        print("📵 Invalid hostname.")

    finally:
        client_socket.close()

    return status


def login_smb(ip, port, username, password):
    smb = SMBConnection(ip, ip)
    smb.login(username, password)


def stuff_smb(ip, port, username, password) -> bool:
    status = False
    try:
        login_smb(ip, port, username, password)
        status = True
    except impacket.smbconnection.SessionError:
        print("⁉️  Could not authenticate user")
    except OSError:
        print("⁉️  Could not connect.")

    return status


def pretty_status(
    ip: str, port: int, user: str, password: str, status: bool
):
    if status:
        print(
            f"✅ Login successful: '{ip}:{port}' with credentials:\n"
            f"🔐 {user}:{password}"
        )
    else:
        print(
            f"❌ Login failed: '{ip}:{port}' with credentials:\n"
            f"🔐 {user}:{password}"
        )


def numbers_to_emojies(number: str) -> str:
    return " ".join([EMOJI_MAP[digit] for digit in number])


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("ip", help="IP to stuff")
    parser.add_argument(
        "-s", "--port", help="Port to stuff, default is all", default=None
    )
    parser.add_argument("-u", "--user", help="Username to use")
    parser.add_argument(
        "-p", "--pass", help="Password to use", dest="password"
    )
    return parser.parse_args()


def main():
    ip = args.ip
    port = args.port
    username = args.user
    password = args.password

    if port:
        return

    for service in Services:
        name = service.name
        port = service.value
        print(f"\n⇝ Testing {name} port: {numbers_to_emojies(str(port))}")
        code = f"stuff_{name.lower()}(ip, port, username, password)"
        status = eval(code)
        pretty_status(ip, port, username, password, status)


if __name__ == "__main__":
    args = parse_args()
    main()
