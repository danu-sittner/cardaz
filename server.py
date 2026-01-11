from __future__ import annotations
import argparse
import sys
import threading
from listener import Listener
from connection import Connection

FAILURE_STATUS_CODE = 1


def handle_client(client_socket: Connection) -> None:
    with client_socket:
        print("recieved message: ", client_socket.receive_message().decode("utf-8"))


def run_server(listener: Listener):
    """
    listens to (server_ip, server_port) if gets connection,
    prints message and closes connection, but keeps listening
    """
    listener.start()
    while True:
        client_socket = listener.accept()
        connection_handler = threading.Thread(
            target=handle_client, args=(client_socket,)
        )
        connection_handler.start()


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Listen for client")
    parser.add_argument("ip", type=str, help="the server's ip")
    parser.add_argument("port", type=int, help="the server's port")
    return parser.parse_args()


def main() -> int:
    """
    Implementation of CLI and sending data to server.
    """
    args = get_args()
    try:
        to_get_listener = Listener(args.ip, args.port)
        run_server(to_get_listener)
        return 1
    except Exception as error:
        print(f"ERROR: {error}")
        return FAILURE_STATUS_CODE


if __name__ == "__main__":
    sys.exit(main())
