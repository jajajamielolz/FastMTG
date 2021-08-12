from fastapi import APIRouter
from fastapi import Request
from app.base import RequiredAuthDependencies
from app.base import NoRequiredAuthDependencies
from typing import Optional
from pydantic import BaseModel
from typing import List
from mtgsdk import Card
from app.utils.abilities import ABILITIES
from mtgsdk import Set
from mtgsdk import Type
from mtgsdk import Supertype
from mtgsdk import Subtype
from mtgsdk import Changelog
from operator import itemgetter
from app.api.deck_builder.utils import get_creatures
from app.api.deck_builder.utils import card_to_dict


router = APIRouter()


@router.get("/find-card", dependencies=NoRequiredAuthDependencies())
def find_card(name: Optional[str] = None, artist: Optional[str] = None, manaCost: Optional[int] = None, power: Optional[int] = None): # noqa!
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

