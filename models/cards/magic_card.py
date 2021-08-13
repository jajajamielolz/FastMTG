import enum

from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy.orm import relationship
from sqlalchemy.types import String
from sqlalchemy_utc import UtcDateTime
from sqlalchemy_utc import utcnow

from models.core.base import Base


class MagicCard(Base):
    __tablename__ = "magic_card"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    mana_cost = Column(String, nullable=False)
    type = Column(String, nullable=False)
    cmc = Column(Integer, nullable=False)
    created_at = Column(UtcDateTime, server_default=utcnow(), nullable=False)

    sub_types_link = relationship("CardHasSubType", back_populates="card")
    sets_link = relationship("CardHasSet", back_populates="card")

    @property
    def color_identity(self):
        return [entry for entry in self.mana_cost if entry in ["W", "U", "R", "G", "B"]]

    @property
    def sets(self):
        return [entry.set for entry in self.sets_link]

    @property
    def subtypes(self):
        return [entry.subtype for entry in self.sub_types_link]

    @property
    def json(self):
        return {
            "name": self.name,
            "mana_cost": self.mana_cost,
            "cmc": self.cmc,
            "color_identity": self.color_identity,
            "type": self.type,
            "sets": self.sets,
            "subtypes": self.subtypes,
        }

    @property
    def display_name(self) -> str:
        return self.id
