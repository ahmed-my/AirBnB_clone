#!/usr/bin/python3
""" Defines all the storage classes in the FileStorage class """
import json
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage():
    """ This represent the storage engine

    Attributes:
        __file_path (str): name of the file where objects are saved
        __objects (dict): instantiated dictionary objects
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ returns the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """ set in __objects the obj key <obj_class_name>.id"""
        objname = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(objname, obj.id)] = obj

    def save(self):
        """ Serializes __objects to the JSON file (path:__file_path file)"""
        file_storage_object = FileStorage.__objects
        objectdict = {obj: file_storage_object[obj].to_dict()
                      for obj in file_storage_object.keys()}
        with open(FileStorage.__file_path, "w") as data:
            json.dump(objectdict, data)

    def reload(self):
        """ Deserializes the JSON file to __objects (only if the JSON file
        (__file_path) exists; otherwise do nothing"""
        try:
            with open(FileStorage.__file_path) as file_data:
                objectdict = json.load(file_data)
                for i in objectdict.values():
                    cls_name = i["__class__"]
                    del i["__class__"]
                    self.new(eval(cls_name)(**i))
        except FileNotFoundError:
            return
