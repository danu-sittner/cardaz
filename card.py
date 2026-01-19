from PIL import Image
from typing import Union, Self
from crypt_image import Cryptimage
from os import PathLike
import struct


def read_u32(buf: bytes, offset: int) -> "tuple[int, int]":
    return struct.unpack_from("<I", buf, offset)[0], offset + 4


def read_bytes(buf: bytes, offset: int, n: int) -> "tuple[bytes, int]":
    return buf[offset : offset + n], offset + n


def read_str(buf: bytes, offset: int) -> "tuple[str, int]":
    n, offset = read_u32(buf, offset)
    b, offset = read_bytes(buf, offset, n)
    return b.decode("utf-8"), offset


def serialize_string(s: str) -> bytes:
    data = s.encode()
    return struct.pack("<I", len(data)) + data


def deserialize_str(offset: int, size: int, all_bytes: bytes) -> str:
    return all_bytes[offset : offset + size].decode()


class Card:
    def __init__(
        self,
        name: str,
        creator: str,
        image: Cryptimage,
        riddle: str,
        solution: Union[str, None],
    ):
        self.name = name
        self.creator = creator
        self.image = image
        self.riddle = riddle
        self.solution = solution

    def __repr__(self) -> str:
        return f"<Card name={self.name}, creator={self.creator}>"

    def __str__(self) -> str:
        status = "<" + self.solution + ">" if self.solution else "unsolved"
        return f"""Card {self.name} by <{self.creator}>
        riddle: <{self.riddle}>
        solution: {status}"""

    @classmethod
    def create_from_path(
        cls,
        name: str,
        creator: str,
        path: Union[str, PathLike],
        riddle: str,
        solution: str,
    ) -> Self:
        return cls(name, creator, Cryptimage.create_from_path(path), riddle, solution)

    def serialize(self) -> bytes:
        serialized_card = b""
        serialized_card += serialize_string(self.name)
        serialized_card += serialize_string(self.creator)
        serialized_card += serialize_string(self.image._image.mode)
        serialized_card += struct.pack("<I", self.image._image.size[0])
        serialized_card += struct.pack("<I", self.image._image.size[1])
        data_bytes = self.image._image.tobytes()
        serialized_card += struct.pack("<I", len(data_bytes))
        serialized_card += data_bytes
        tag = self.image._tag or b""
        serialized_card += struct.pack("<I", len(tag))
        serialized_card += tag
        key_hash = self.image._key_hash or b""
        serialized_card += struct.pack("<I", len(key_hash)) + key_hash
        serialized_card += serialize_string(self.riddle)
        return serialized_card

    @classmethod
    def deserialize(cls, serialized_bytes: bytes) -> Self:
        offset = 0
        name, offset = read_str(serialized_bytes, offset)
        creator, offset = read_str(serialized_bytes, offset)
        mode, offset = read_str(serialized_bytes, offset)
        length, offset = read_u32(serialized_bytes, offset)
        width, offset = read_u32(serialized_bytes, offset)
        data_size, offset = read_u32(serialized_bytes, offset)
        data, offset = read_bytes(serialized_bytes, offset, data_size)
        tag, offset = read_u32(serialized_bytes, offset)
        key_hash_size, offset = read_u32(serialized_bytes, offset)
        key_hash, offset = read_bytes(serialized_bytes, offset, key_hash_size)
        riddle, offset = read_str(serialized_bytes, offset)
        return cls(
            name,
            creator,
            Cryptimage(Image.frombytes(mode, (length, width), data), key_hash, tag),
            riddle,
            None,
        )
