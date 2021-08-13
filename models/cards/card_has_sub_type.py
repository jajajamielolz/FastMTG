from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import String

from models.core.base import Base


class CardHasSubType(Base):
    __tablename__ = "card_has_sub_type"

    id = Column(String, primary_key=True)
    card_id = Column(String, ForeignKey("magic_card.id"), nullable=False)
    sub_type_id = Column(String, ForeignKey("sub_type.id"), nullable=False)

    subtype = relationship("SubType", back_populates="cards_link")
    card = relationship("MagicCard", back_populates="sub_types_link")
