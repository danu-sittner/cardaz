from __future__ import annotations
import argparse
import sys
from connection import Connection

FAILURE_STATUS_CODE = 1


def send_data(server_ip: str, server_port: int, data: str) -> None:
    """
    Send data to server in address (server_ip, server_port).
    """
    with Connection.connect(server_ip, server_port) as to_send_connection:
        print("sending message...")
        to_send_connection.send_message(data.encode("utf-8"))


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send data to server.")
    parser.add_argument("server_ip", type=str, help="the server's ip")
    parser.add_argument("server_port", type=int, help="the server's port")
    parser.add_argument("data", type=str, help="the data")
    return parser.parse_args()


def main() -> int:
    """
    Implementation of CLI and sending data to server.
    """
    args = get_args()
    try:
        send_data(args.server_ip, args.server_port, args.data)
        print("Done.")
        return 0
    except Exception as error:
        print(f"ERROR: {error}")
        return FAILURE_STATUS_CODE


if __name__ == "__main__":
    sys.exit(main())
