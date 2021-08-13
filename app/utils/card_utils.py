import uuid

from mtgsdk import Card

from models import CardHasSet
from models import CardHasSubType
from models import FastMTGDB
from models import MagicCard
from models import MagicSet
from models import SubType


def upload_card(card: Card):
    db = FastMTGDB().get_mtg_db()
    name = card.name
    mana_cost = card.mana_cost
    card_type = card.type
    cmc = card.cmc
    card_dict = {"name": name, "mana_cost": mana_cost, "type": card_type, "cmc": cmc}

    db_card = db.query(MagicCard).where(MagicCard.name == name).first()
    if not card:
        uid = str(uuid.uuid4())
        db_card = MagicCard(id=uid, **card_dict)
        db.add(db_card)
        db.commit()

    set = card.set
    db_set = db.query(MagicSet).where(MagicSet.name == set).first()
    if not db_set:
        uid = str(uuid.uuid4())
        db_set = MagicSet(id=uid, name=set)
        db.add(db_set)
        db.commit()

    card_has_set = (
        db.query(CardHasSet)
        .where(CardHasSet.card_id == db_card.id, CardHasSet.set_id == db_set.id)
        .first()
    )
    if not card_has_set:
        uid = str(uuid.uuid4())
        db_set = CardHasSet(id=uid, card_id=db_card.id, set_id=db_set.id)
        db.add(db_set)
        db.commit()

    subtypes = card.subtypes
    for subtype in subtypes:
        db_subtype = db.query(SubType).where(SubType.name == subtype).first()
        if not db_subtype:
            uid = str(uuid.uuid4())
            db_subtype = SubType(id=uid, name=subtype)
            db.add(db_subtype)
            db.commit()

        card_has_subtype = (
            db.query(CardHasSubType)
            .where(
                CardHasSubType.card_id == db_card.id,
                CardHasSubType.sub_type_id == db_subtype.id,
            )
            .first()
        )
        if not card_has_subtype:
            uid = str(uuid.uuid4())
            card_has_subtype = CardHasSubType(
                id=uid, card_id=db_card.id, sub_type_id=db_subtype.id
            )
            db.add(card_has_subtype)
            db.commit()

    return


cards = Card.where(
    types="Creature", colorIdentity="R", rarity="mythic", text="demon"
).all()

if cards:
    card = cards[1]

upload_card(card)
