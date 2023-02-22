#!/usr/bin/python3

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import os

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        HBNB_MYSQL_USER = os.getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = os.getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = os.getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = os.getenv('HBNB_MYSQL_DB')
        HBNB_ENV = os.getenv('HBNB_ENV')

        try:
            self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:3306/{}'
                                          .format(HBNB_MYSQL_USER,
                                                  HBNB_MYSQL_PWD,
                                                  HBNB_MYSQL_HOST,
                                                  HBNB_MYSQL_DB),
                                          pool_pre_ping=True)
            if HBNB_ENV == 'test':
                Base.metadata.drop_all(bind=self.__engine)
        except Exception:
            raise
            print("Not Found")
            
    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def delete(self, obj=None):
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        sess = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess)
        self.__session = Session()

    def close(self):
        """Close SQLAlchemy session."""
        self.__session.close()


    def get(self, cls, id):
        """returns the object based on the class and its ID,
        or None if not found"""
        if cls is not None and id is not None:
            classes = self.all(cls)
            for obj in classes.values():
                if obj.id == id:
                    return obj
        else:
            return None

    def count(self, cls=None):
        """count the number of objects in storage"""
        return len(self.all(cls))