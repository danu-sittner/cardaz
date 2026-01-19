from __future__ import annotations
import argparse
import sys
from os import PathLike
from connection import Connection
from card import Card

FAILURE_STATUS_CODE = 1


def send_card(
    server_ip: str,
    server_port: int,
    name: str,
    creator: str,
    riddle: str,
    solution: str,
    path: PathLike,
) -> None:
    """
    Send card to server in address (server_ip, server_port).
    """
    with Connection.connect(server_ip, server_port) as to_send_connection:
        to_send = Card.create_from_path(name, creator, path, riddle, solution)
        print(to_send.solution, len(to_send.solution))
        to_send.image.encrypt(solution)
        to_send_connection.send_message(to_send.serialize())


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Send data to server.")
    parser.add_argument("server_ip", type=str, help="the server's ip")
    parser.add_argument("server_port", type=int, help="the server's port")
    parser.add_argument("name", type=str, help="the card's name")
    parser.add_argument("creator", type=str, help="the card's creator")
    parser.add_argument("riddle", type=str, help="the card's riddle")
    parser.add_argument("solution", type=str, help="the riddle's solution")
    parser.add_argument("path", type=str, help="the image's path")
    return parser.parse_args()


def main() -> int:
    """
    Implementation of CLI and sending data to server.
    """
    args = get_args()
    try:
        send_card(
            args.server_ip,
            args.server_port,
            args.name,
            args.creator,
            args.riddle,
            args.solution,
            args.path,
        )
        print("Done.")
        return 0
    except Exception as error:
        print(f"ERROR: {error}")
        return FAILURE_STATUS_CODE


if __name__ == "__main__":
    sys.exit(main())
