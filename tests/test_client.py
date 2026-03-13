from __future__ import annotations

from unittest.mock import MagicMock
import pytest

from client import send_card
from connection import Connection
from card import Card


def test_send_card_happy_path(monkeypatch: pytest.MonkeyPatch) -> None:
    conn = MagicMock()
    conn.__enter__.return_value = conn
    connect_mock = MagicMock(return_value=conn)
    monkeypatch.setattr(Connection, "connect", connect_mock)

    fake_card = MagicMock(name="card")

    fake_card.image = MagicMock(name="image")

    fake_card.serialize.return_value = b"SERIALIZED_CARD"

    monkeypatch.setattr(Card, "create_from_path", MagicMock(return_value=fake_card))

    send_card(
        server_ip="127.0.0.1",
        server_port=5555,
        name="Guernica",
        creator="Picasso",
        riddle="When was it painted?",
        solution="1937",
        path="/home/dolev/guernica.jpeg",
    )
    connect_mock.assert_called_once_with("127.0.0.1", 5555)

    fake_card.serialize.assert_called_once()

    conn.send_message.assert_called_once_with(b"SERIALIZED_CARD")


def test_send_card_raises_if_connect_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(Connection, "connect", MagicMock(side_effect=OSError("boom")))
    with pytest.raises(OSError, match="boom"):
        send_card("127.0.0.1", 5555, "n", "c", "r", "s", "/home/dolev/x.jpeg")
