from __future__ import annotations
import argparse
import sys
import socket
import struct
import threading

LITTLE_ENDIAN_LEN_SIZE = 4
FAILURE_STATUS_CODE = 1


def get_message(client_socket: socket) -> None:
    packed = recv_exact(client_socket, LITTLE_ENDIAN_LEN_SIZE)
    if not packed:
        return
    msg_len = struct.unpack("<I", packed)[0]
    data = recv_exact(client_socket, msg_len)

    print("recieved message: ", data.decode("utf-8"))


def recv_exact(sock: socket, length: int) -> bytes:
    data = b""
    while len(data) < length:
        chunk = sock.recv(length - len(data))
        if not chunk:
            raise ConnectionError("Connection closed")
        data += chunk
    return data


def run_server(ip: str, port: int):
    """
    listens to (server_ip, server_port) if gets connection,
    prints message and closes connection, but keeps listening
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen()

    while True:
        client_socket = server_socket.accept()[0]
        connection_handler = threading.Thread(target=get_message, args=(client_socket,))
        connection_handler.start()
        client_socket.close()


def get_args():
    parser = argparse.ArgumentParser(description="Listen for client")
    parser.add_argument("ip", type=str, help="the server's ip")
    parser.add_argument("port", type=int, help="the server's port")
    return parser.parse_args()


def main():
    """
    Implementation of CLI and sending data to server.
    """
    args = get_args()
    try:
        run_server(args.ip, args.port)
    except Exception as error:
        print(f"ERROR: {error}")
        return FAILURE_STATUS_CODE


if __name__ == "__main__":
    sys.exit(main())
