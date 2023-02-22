#!/usr/bin/python3
""" State Module """
from models.base_model import Base, BaseModel
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models


class State(BaseModel, Base):
    """
    BaseMdel sub class
    """

    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship('City', backref='state', cascade='delete')

    # if ("HBNB_TYPE_STORAGE", None) == None:
    @property
    def cities(self):
        Clist = []
        for city in list(models.storage.all(City).values()):
            if city.state_id == self.id:
                Clist.append(city)
        return Clist
