from mtgsdk import Card


rarities = ["mythic", "rare", "uncommon", "common"]


def get_spells(
    spell_type,
    subtypes,
    num_cards,
    abilities,
    deck_list=None,
    color_identity=None,
    land_set="LRW",
):
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
                if num_cards == 0:
                    break
                cards = Card.where(
                    types=spell_type, colorIdentity=color, rarity=rarity, text=subtype
                ).all()
                for card in cards:
                    deck_list, num_cards = check_and_add_card(
                        card, color_identity, deck_list, num_cards, card_names
                    )
                    if num_cards == 0:
                        break

        # go through colors
        for color in color_identity:
            if num_cards == 0:
                break
            # find cards with mentions of abilities
            for ability in abilities:
                if num_cards == 0:
                    break
                cards = Card.where(
                    types=spell_type, colorIdentity=color, rarity=rarity, text=ability
                ).all()
                for card in cards:
                    deck_list, num_cards = check_and_add_card(
                        card, color_identity, deck_list, num_cards, card_names
                    )
                    if num_cards == 0:
                        break
                if num_cards == 0:
                    break
    if spell_type == "Land" and num_cards > 0:
        deck_list = top_up_basics(num_cards, color_identity, deck_list, land_set)

    return deck_list


def get_creatures(
    subtypes, num_creatures, abilities, deck_list=None, color_identity=None
):
    deck_list_names = [creature.name for creature in deck_list]
    # get creatures
    if deck_list is None:
        deck_list = []
    if color_identity is None:
        color_identity = ["W", "U", "B", "R", "G", None]
    for sub_type in subtypes:
        if num_creatures == 0:
            break
        for color in color_identity:
            if num_creatures == 0:
                break
            creatures = Card.where(
                subtypes=sub_type, types="Creature", colorIdentity=color
            ).all()
            # cherry pick ones with similar abilities
            for creature in creatures:
                if num_creatures == 0:
                    break
                # only consider if the card isn't in the list and meets color identity restriction
                if creature.name not in deck_list_names and (
                    all(x in color_identity for x in creature.color_identity)
                ):
                    for ability in abilities:
                        if creature.text:
                            if ability in creature.text:
                                deck_list.append(creature)
                                deck_list_names.append(creature.name)
                                num_creatures -= 1
                                break

    # if there still room for cards, fill with mythic/rare/uncommon cards of the type
    if num_creatures != 0:
        for rarity in rarities:
            for sub_type in subtypes:
                if num_creatures != 0:
                    for color in color_identity:
                        creatures = Card.where(
                            subtypes=sub_type,
                            types="Creature",
                            colorIdentity=color,
                            rarity=rarity,
                        ).all()
                        # cherry pick ones with similar abilities
                        for creature in creatures:
                            if num_creatures == 0:
                                break
                            # only consider if the card isn't in the list and meets color identity restriction
                            if creature.name not in deck_list_names and (
                                all(
                                    x in color_identity for x in creature.color_identity
                                )
                            ):
                                deck_list.append(creature)
                                deck_list_names.append(creature.name)
                                num_creatures -= 1
    return deck_list


def card_to_dict(card):
    response = {
        "name": card.name,
        "mana_cost": card.mana_cost,
        "cmc": card.cmc,
        "color_identity": card.color_identity,
        "type": card.type,
        "set": card.set,
    }
    return response


def check_and_add_card(card, color_identity, deck_list, num_cards, card_names):
    if card.name not in card_names and (
        all(c in color_identity for c in card.color_identity)
    ):
        deck_list.append(card)
        card_names.append(card.name)
        num_cards -= 1
    return deck_list, num_cards


def top_up_basics(num_cards, color_identity, deck_list, land_set):

    num_basic_land = int(num_cards / len(color_identity))
    for color in color_identity:
        if color == "U":
            lands_left = num_basic_land
            while lands_left:
                if lands_left == 0:
                    break
                lands = Card.where(
                    types="Land", colorIdentity=color, set=land_set, name="Island"
                ).all()
                for land in lands:
                    deck_list.append(land)
                    lands_left -= 1
                    num_cards -= 1
                    if lands_left == 0:
                        break
        if color == "W":
            lands_left = num_basic_land
            while lands_left:
                if lands_left == 0:
                    break
                lands = Card.where(
                    types="Land", colorIdentity=color, set=land_set, name="Plain"
                ).all()
                for land in lands:
                    deck_list.append(land)
                    lands_left -= 1
                    num_cards -= 1
                    if lands_left == 0:
                        break
        if color == "B":
            lands_left = num_basic_land
            while lands_left:
                if lands_left == 0:
                    break
                lands = Card.where(
                    types="Land", colorIdentity=color, set=land_set, name="Swamp"
                ).all()
                for land in lands:
                    deck_list.append(land)
                    lands_left -= 1
                    num_cards -= 1
                    if lands_left == 0:
                        break
        if color == "R":
            lands_left = num_basic_land
            while lands_left:
                if lands_left == 0:
                    break
                lands = Card.where(
                    types="Land", colorIdentity=color, set=land_set, name="Mountain"
                ).all()
                for land in lands:
                    deck_list.append(land)
                    lands_left -= 1
                    num_cards -= 1
                    if lands_left == 0:
                        break
        if color == "G":
            lands_left = num_basic_land
            while lands_left:
                if lands_left == 0:
                    break
                lands = Card.where(
                    types="Land", colorIdentity=color, set=land_set, name="Forest"
                ).all()
                for land in lands:
                    deck_list.append(land)
                    lands_left -= 1
                    num_cards -= 1
                    if lands_left == 0:
                        break
    if num_cards:
        lands = Card.where(name="Commander's Sphere").all()
        deck_list.append(lands[0])
    return deck_list
