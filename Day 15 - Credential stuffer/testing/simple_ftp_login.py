import socket

ip = "0.0.0.0"
port = 21
username = "vsftp"
password = "Ekstragol2"


def login_ftp(target):
    try:
        server = (target, 21)
        user = f"USER {username}\r\n"
        pwd = f"PASS {password}\r\n"

        sock = socket.socket()
        sock.connect(server)

        sock.recv(4096)
        sock.sendall(user.encode())

        sock.recv(4096)
        sock.sendall(pwd.encode())

        answer = sock.recv(4096).decode("utf-8")

        if "230" in answer:
            print("Found FTP!")

        elif "530" in answer:
            sock.close()

        sock.close()
    except:
        print("Login failed!\n")


login_ftp(ip)
