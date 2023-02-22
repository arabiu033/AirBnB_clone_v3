#!/usr/bin/python3
""" File Storage Module """
import json
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """
    class FileStorage that serializes instances to a
    JSON file and deserializes JSON file to instances:
    """
    __file_path = "file.json"
    __objects = {}
    __classes = {"BaseModel": BaseModel, "User": User, "Place": Place,
                 "State": State, "City": City, "Amenity": Amenity,
                 "Review": Review}

    def all(self, cls=None):
        """
        returns the dictionary __objects
        """
        if cls is not None:
            if cls in FileStorage.__classes:
                cls = FileStorage.__classes[cls]
            objs = {}
            for key, val in FileStorage.__objects.items():
                if type(val) == cls:
                    objs[key] = val
            return objs

        return FileStorage.__objects

    def new(self, obj):
        """
        sets in __objects the obj with key <obj class name>.id
        """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """
        serializes __objects to the JSON file (path: __file_path)
        """
        copy = FileStorage.__objects.copy()
        for k in copy.keys():
            copy[k] = copy[k].to_dict()
        with open(FileStorage.__file_path, "w", encoding="utf-8") as fil:
            json.dump(copy, fil)

    def reload(self):
        """
        deserializes the JSON file to __objects
        (only if the JSON file (__file_path) exists
        """
        try:
            with open(FileStorage.__file_path, "r", encoding="utf-8") as fil:
                copy = json.load(fil)
            for k in copy.keys():
                v = k.split(".")
                copy[k] = FileStorage.__classes[v[0]](**(copy[k]))
            FileStorage.__objects = copy
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Delete an object from the list of objects if it exists
        """
        try:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            del FileStorage.__objects[key]
        except Exception:
            pass

    def close(self):
        """reload method."""
        self.reload()
