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
from app.api.deck_builder.utils import get_spells

router = APIRouter()


@router.get("/build-deck", dependencies=NoRequiredAuthDependencies())
def deck_build(commander: Optional[str] = None, total_lands: Optional[int] = 34, total_creatures: Optional[int] = 35, total_artifacts: Optional[int] = 6, total_sorcery: Optional[int] = 7, total_enchantments: Optional[int] = 6, total_walkers: Optional[int] = 1, total_instants: Optional[int] = 9, basic_land_set: Optional[str] = "LRW"):
    """
    Given a legendary creature, build a commander deck around it.
    Optional parameters: \n
    total_lands -> By default 34 \n
    total_creatures -> By default 35 \n
    total_artifacts -> By default 6 \n
    total_sorcery -> By default 7 \n
    total_enchantments -> By default 6 \n
    total_walkers -> By default 1 \n
    basic_land_set -> Set for basic lands \n

    """
    # initialize commander
    commander = Card.where(name=commander).all()
    commander = commander[0]
    deck_list = [commander]

    # extract commander features
    subtypes = commander.subtypes
    abilities = [ability for ability in ABILITIES if ability in commander.text.lower()]

    color_identity = commander.color_identity

    # get creatures
    if total_creatures:
        deck_list = get_creatures(subtypes, total_creatures, abilities, deck_list, color_identity)

    # get artifacts
    if total_artifacts:
        deck_list = get_spells(spell_type="Artifact", subtypes=subtypes, num_cards=total_artifacts, abilities=abilities, deck_list=deck_list, color_identity=color_identity)

    # get sorcerys
    if total_sorcery:
        deck_list = get_spells(spell_type="Sorcery", subtypes=subtypes, num_cards=total_sorcery, abilities=abilities, deck_list=deck_list, color_identity=color_identity)

    # get enchantments
    if total_enchantments:
        deck_list = get_spells(spell_type="Enchantment", subtypes=subtypes, num_cards=total_enchantments, abilities=abilities, deck_list=deck_list, color_identity=color_identity)

    # get instants
    if total_instants:
        deck_list = get_spells(spell_type="Instant", subtypes=subtypes, num_cards=total_instants, abilities=abilities, deck_list=deck_list, color_identity=color_identity)

    # get planeswalkers
    if total_walkers:
        deck_list = get_spells(spell_type="Planeswalker", subtypes=subtypes, num_cards=total_walkers, abilities=abilities, deck_list=deck_list, color_identity=color_identity)

    # get lands
    if total_lands:
        deck_list = get_spells(spell_type="Land", subtypes=subtypes, num_cards=total_lands, abilities=abilities, deck_list=deck_list, color_identity=color_identity, land_set=basic_land_set)

    cards = [card.name for card in deck_list]
    for card in cards:
        print(card)

    return {"status": "success", "result": cards}

