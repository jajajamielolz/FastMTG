import mtgsdk
from mtgsdk import Card
from mtgsdk import Set
from mtgsdk import Type
from mtgsdk import Supertype
from mtgsdk import Subtype
from mtgsdk import Changelog


def check_and_add_card(card, color_identity, deck_list, num_cards, card_names):
    if card.name not in card_names and (all(c in color_identity for c in card.color_identity)):
        deck_list.append(card)
        card_names.append(card.name)
        num_cards -= 1
    return deck_list, num_cards

card_name = "Vengevine"

subtypes = ["elf", "goblin"]
num_lands = 3
abilities = ["haste", "lifelink"]
color_identity = ["G", "R", "B"]
rarities = ["mythic", "rare", "uncommon", "basic"]

deck_list = []

num_cards = 3

card_names = []
# in order of rarity
for rarity in rarities:
    if num_cards == 0:
        break
    # go through colors
    for color in color_identity:
        if num_cards == 0:
            break
        # find cards with mentions of subtypes
        for subtype in subtypes:
            lands = Card.where(types="Land", colorIdentity=color, rarity=rarity, text=subtype).all()
            for card in lands:
                deck_list, num_cards = check_and_add_card(card, color_identity, deck_list, num_cards, card_names)
                if num_cards == 0:
                    break

    # go through colors
    for color in color_identity:
        if num_cards == 0:
            break
        # find cards with mentions of abilities
        for ability in abilities:
            lands = Card.where(types="Land", colorIdentity=color, rarity=rarity, text=ability).all()
            if num_cards == 0:
                break
    print("o")






print("")