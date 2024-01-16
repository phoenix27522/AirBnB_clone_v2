#!/usr/bin/python3
"""Defines the FileStorage class."""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import shlex


class FileStorage:
    """class that stores info and help to serialize and desrialize.

    Attributes:
        __file_path(str): the name of the file to the objects to.
        __objects(dict): A dictionary of instantiated objects.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self, cls =None):
        """Returns the dictionary of __objects."""
        dic = {}
        if cls:
            dictionary = self.__objects
            for key in dictionary:
                part = key.replace('.', ' ')
                part = shlex.split(part)
                if (part[0] == cls.__name__):
                    dic[key] = self.__objects[key]
                return (dic)
        else:
            return self.__objects

    def new(self, obj):
        """Sets a unique identifier "id" """
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """Serialize the __objects to a JSON file."""
        with open(FileStorage.__file_path, "w") as file:
            json.dump({k: v.to_dict() for k, v in self.__objects.items()}, file)


    def reload(self):
        """Deserialize the json file """
        try:
            with open(FileStorage.__file_path) as file:
                new_dict = json.load(file)
                for i in new_dict.values():
                    name_cls = i["__class__"]
                    del i["__class__"]
                    self.new(eval(name_cls)(**i))
        except FileNotFoundError:
            return

    def delete(self, obj=None):
        """ deleting existing element"""
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            del self.__objects[key]
