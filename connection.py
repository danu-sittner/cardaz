from __future__ import annotations
import socket
import struct

LITTLE_ENDIAN_LEN_SIZE = 4


def recv_exact(sock: socket.socket, length: int) -> bytes:
    data = b""
    while len(data) < length:
        chunk = sock.recv(length - len(data))
        if not chunk:
            raise ConnectionError("Connection closed")
        data += chunk
    return data


class Connection:
    def __init__(self, connection: socket.socket) -> None:
        self._connection = connection

    def __repr__(self) -> str:
        return f"<Connection from {self._connection.getsockname()[0]}:{self._connection.getsockname()[1]} to {self._connection.getpeername()[0]}:{self._connection.getpeername()[1]}>"

    def send_message(self, message: bytes) -> None:
        self._connection.sendall(struct.pack("<I", len(message)))
        self._connection.sendall(message)

    def receive_message(self) -> bytes:
        packed = recv_exact(self._connection, LITTLE_ENDIAN_LEN_SIZE)
        msg_len = struct.unpack("<I", packed)[0]
        return recv_exact(self._connection, msg_len)

    @classmethod
    def connect(cls, host: str, port: int) -> Connection:
        return cls(socket.create_connection((host, port)))

    def close(self) -> None:
        self._connection.close()

    def __enter__(self) -> Connection:
        return self

    def __exit__(self, exception_type, exception, traceback) -> None:
        self.close()
