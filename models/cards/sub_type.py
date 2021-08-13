from sqlalchemy import Column
from sqlalchemy.orm import relationship
from sqlalchemy.types import String

from models.core.base import Base


class SubType(Base):
    __tablename__ = "sub_type"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)

    cards_link = relationship("CardHasSubType", back_populates="subtype")
