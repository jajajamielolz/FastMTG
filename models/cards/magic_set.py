from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.types import String

from models.core.base import Base


class MagicSet(Base):
    __tablename__ = "magic_set"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)

    cards_link = relationship("CardHasSet", back_populates="set")
