from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import String

from models.core.base import Base


class CardHasSet(Base):
    __tablename__ = "card_has_set"

    id = Column(String, primary_key=True)
    card_id = Column(String, ForeignKey("magic_card.id"), nullable=False)
    set_id = Column(String, ForeignKey("magic_set.id"), nullable=False)

    set = relationship("MagicSet", back_populates="cards_link")
    card = relationship("MagicCard", back_populates="sets_link")
