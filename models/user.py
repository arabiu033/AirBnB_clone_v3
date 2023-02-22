#!/usr/bin/python3
"""This is the user class."""
from hashlib import md5
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models
from models.base_model import BaseModel, Base


class User(BaseModel, Base):
    """This is the class for user
    Attributes:
        email: email address
        password: password for you login
        first_name: first name
        last_name: last name
    """
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))
    reviews = relationship('Review', backref='user',
                           cascade='delete')
    places = relationship('Place', backref='user',
                          cascade='delete')

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, __name, __value):
        """Encrypt user password"""
        if __name == "password":
            __value = md5(__value.encode()).hexdigest()
        return super().__setattr__(__name, __value)