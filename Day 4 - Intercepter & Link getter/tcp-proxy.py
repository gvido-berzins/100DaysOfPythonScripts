from enum import Enum
import socket
import threading
import argparse
import traceback
import binascii
import json


def jp(data):
    print(json.dumps(data, indent=2))


def hexdump(src, length=16):
    src = bytes(src, "utf-8")
    result = []
    digits = 4 if isinstance(src, str) else 2

    for i in range(0, len(src), length):
        s = src[i:i+length]

        data = ['%0*X' % (digits, int(x)) for x in s]
        hexa = ' '.join(data)

        data = [chr(x) if 0x20 <= x < 0x7F else '.' for x in s]
        text = ''.join(data)

        result.append(
            "%04X   %-*s   %s" % (i, length * (digits+1), hexa, text))

    print('\n'.join(result))


class Direction(Enum):
    SEND = 'Send'
    RECEIVE = 'Receive'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("lhost")
    parser.add_argument("lport", type=int)
    parser.add_argument("rhost")
    parser.add_argument("rport", type=int)
    parser.add_argument("--receive", action="store_true", default=True)
    return parser.parse_args()


def print_connection(host, port, direction: Direction):
    if direction == Direction.RECEIVE:
        print(f"--> receiving incoming connection from '{host}:{port}'")
    elif direction == Direction.SEND:
        print(f"<-- sending outgoing connection to '{host}:{port}'")


def sendm(socket, data):
    data = bytes(data, "utf-8")
    socket.send(data)


def server_loop(lhost, lport, rhost, rport, receive_first: bool):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((lhost, lport))
    except socket.error:
        traceback.print_exc()
        print(f"failed to listen on '{lhost}:{lport}'")
        print("Check for listening scokets or permissions")
        exit()

    print(f"Listening on '{lhost}:{lport}'")
    server.listen(5)

    try:
        while True:
            client_socket, addr = server.accept()
            print_connection(addr[0], addr[1], Direction.RECEIVE)
            start_proxy_thread(client_socket, rhost, rport, receive_first)
    except KeyboardInterrupt:
        print('x - Keyboard interrupt - x')
        server.close()


def start_proxy_thread(client_socket, rhost, rport, receive_first):
    proxy_thread = threading.Thread(
        target=proxy_handler,
        args=(client_socket, rhost, rport, receive_first)
    )
    proxy_thread.start()


def proxy_handler(client_socket, rhost, rport, receive_first):
    print(rhost, rport)

    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((rhost, rport))

    if receive_first:
        print('< Receiving First >')
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)
        remote_buffer = response_handler(remote_buffer)

        if len(remote_buffer):
            print(f"<-- sending {len(remote_buffer)} bytes to localhost")
            sendm(client_socket, remote_buffer)

    while True:
        local_buffer = receive_from(client_socket, 10)

        if len(local_buffer):
            print(f"--> received {len(local_buffer)} bytes from localhost")
            hexdump(local_buffer)

            local_buffer = request_handler(local_buffer)
            sendm(remote_socket, local_buffer)
            print("--> Sent to remote")

        remote_buffer = receive_from(remote_socket)

        if len(remote_buffer):
            print(f"<-- Received {len(remote_buffer)} bytes from remote")
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)

            sendm(client_socket, remote_buffer)
            print("<-- Sent to localhost")

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("X No more data. Connection closed.")
            break


def receive_from(connection, timeout=2):
    """Perform buffer modifications"""
    data_buffer = ""
    connection.settimeout(timeout)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            data_buffer += data.decode("utf-8")
    except socket.timeout:
        pass

    return data_buffer


def request_handler(buffer):
    """Perform buffer modifications"""
    return buffer


def response_handler(buffer):
    """Perform packet mofications"""
    return buffer


def create_connection(host, port):
    csocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    csocket.connect((host, port))
    return csocket


def main():
    server_loop(
        args.lhost,
        args.lport,
        args.rhost,
        args.rport,
        args.receive
    )


if __name__ == "__main__":
    args = parse_args()
    main()
