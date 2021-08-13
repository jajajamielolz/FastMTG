from typing import Optional

from fastapi import APIRouter
from mtgsdk import Card

from app.api.deck_builder.utils import card_to_dict
from app.base import NoRequiredAuthDependencies


router = APIRouter()


@router.get("/find-card", dependencies=NoRequiredAuthDependencies())
def find_card(
    name: Optional[str] = None,
    artist: Optional[str] = None,
    manaCost: Optional[int] = None,
    power: Optional[int] = None,
):  # noqa!
    card_dict = {}
    if name:
        card_dict["name"] = name
    if manaCost:
        card_dict["mana_cost"] = manaCost
    if power:
        card_dict["power"] = power
    if artist:
        card_dict["artist"] = artist

    cards = Card.where(**card_dict).all()

    response = [card_to_dict(card) for card in cards]

    return {"status": "success", "result": response}
