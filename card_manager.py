from card import Card
from pathlib import Path
from typing import Union
from os import PathLike
from crypt_image import Cryptimage
import json


class CardManager:
    @staticmethod
    def save(card: Card, dir_path: Union[str, PathLike] = "."):
        Path(f"{dir_path}/{CardManager.get_identifier(card)}").mkdir(
            parents=True, exist_ok=True
        )
        with open(
            f"{dir_path}/{CardManager.get_identifier(card)}/metadata.json", "w"
        ) as f:
            json.dump(
                {
                    "name": card.name,
                    "creator": card.creator,
                    "image path": f"{dir_path}/{CardManager.get_identifier(card)}/image.bin",
                    "riddle": card.riddle,
                    "solution": card.solution,
                },
                f,
            )
        card.image.save_to_file(
            f"{dir_path}/{CardManager.get_identifier(card)}/image.bin"
        )

    @staticmethod
    def get_identifier(card: Card) -> str:
        return f"{card.name}_by_{card.creator}"

    @staticmethod
    def load(identifier: str) -> Card:
        with open(identifier, "r") as f:
            data = json.load(f)
        return Cryptimage.load_from_file(
            data["name"],
            data["creator"],
            data["image path"],
            data["riddle"],
            data["solution"],
        )
