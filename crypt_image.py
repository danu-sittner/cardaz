from PIL import Image
import hashlib
from Crypto.Cipher import AES
from typing import Self, Optional
from os import PathLike


class Cryptimage:
    def __init__(
        self, image: Image.Image, key_hash: Optional[bytes], tag: Optional[bytes] = None
    ) -> None:
        self._image = image
        self._key_hash = key_hash
        self._tag = tag

    @staticmethod
    def _derive_key(key: str) -> bytes:
        return hashlib.sha256(hashlib.sha256(key.encode("utf-8")).digest()).digest()

    @classmethod
    def create_from_path(cls, path: str | PathLike[str]) -> Self:
        with Image.open(path) as im:
            im.load()
            return cls(im.copy(), None)

    def encrypt(self, key: str) -> None:
        self._key_hash = self._derive_key(key)
        cipher = AES.new(self._key_hash, AES.MODE_EAX, nonce=b"arazim")
        bytes_cipher, self._tag = cipher.encrypt_and_digest(self._image.tobytes())
        self._image = Image.frombytes(self._image.mode, self._image.size, bytes_cipher)

    def decrypt(self, key: str) -> bool:
        derived = self._derive_key(key)
        if self._key_hash is None or derived != self._key_hash:
            return False
        if self._tag is None:
            return False

        cipher = AES.new(self._key_hash, AES.MODE_EAX, nonce=b"arazim")
        try:
            pt = cipher.decrypt_and_verify(self._image.tobytes(), self._tag)
        except ValueError:
            return False

        self._image = Image.frombytes(self._image.mode, self._image.size, pt)
        self._key_hash = None
        self._tag = None
        return True
