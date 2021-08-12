import re

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr


class Base(object):
    """Base model.

    Sets up inheritance from sqlalchemy and adds an as_dict function
    for all other models.
    """

    @declared_attr
    def __tablename__(cls):
        name = re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()
        return name

    exemption_values = {"_sa_instance_state"}


Base = declarative_base(cls=Base)

Base.as_dict = lambda self: {
    k: v for k, v in self.__dict__.items() if k not in self.exemption_values
}

Base.as_return = lambda self: {
    k: v
    for k, v in self.__dict__.items()
    if k not in (self.exemption_values | {"password"})
}

Base.__repr__ = lambda self: f"{type(self).__name__}: {self.as_dict()}"
