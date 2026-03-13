from __future__ import annotations
import socket
from connection import Connection


class Listener:
    def __init__(self, host: str, port: int, backlog: int = 1000) -> None:
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._host = host
        self._port = port
        self._backlog = backlog

    def __repr__(self) -> str:
        return (
            f"Listener(port={self._port}, host={self._host}, backlog={self._backlog})"
        )

    def start(self) -> None:
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind((self._host, self._port))
        self._server_socket.listen(self._backlog)

    def stop(self) -> None:
        self._server_socket.close()

    def accept(self) -> Connection:
        return Connection(self._server_socket.accept()[0])

    def __enter__(self) -> Listener:
        return self

    def __exit__(self) -> None:
        self.stop()
