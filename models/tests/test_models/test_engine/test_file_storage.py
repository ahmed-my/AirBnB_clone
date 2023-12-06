#!/usr/bin/python3
""" Defines unittests for models.engine.file_storage.py

Unittest classes():
    TestFileStorage_instantiatin
    TestFileStorage_methods """

import os
import json
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.amenity import Aminity
from models.city import City
from models.place import Place
from models.review import review
from models.state import State
from model.user import User


class TestFileStorage_instantiation(unittest.TestCase):
    """
        Unittests for testing instantiation of the FileStorage class"""

    def test_FileStorage_instantiation_no_args(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_FileStorage_instanstiation_with_args(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_FileStorage_file_path_is_private_str(self):
        self.assertEqual(str, type(FileStorage._FileStorage__objects))

    def test_storage_initializes(self):
        self.assertEqual(type(models.storage), FileStorage)


class TestFileStorage_methods(unittest.TestCase):
    """ Unittests for methods testing of the FileStorage class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new(self):
        b_m = BaseModel()
        a = Aminity()
        c = City()
        p = Place()
        s = State()
        r = Review()
        u = User()
        models.storage.new(b_m)
        models.storage.new(a)
        models.storage.new(c)
        models.storage.new(p)
        models.storage.new(s)
        models.storage.new(r)
        models.storage.new(u)
        self.assertIn("BaseModel." + b_m.id, models.storage.all().key())
        self.assertIn(b_m, models.storage.all().values())
        self.assertIn("Aminity." + a.id, models.storage.all().key())
        self.assertIn(a, models.storage.all().values())
        self.assertIn("city." + c.id, models.storage.all().key())
        self.assertIn(c, models.storage.all().values())
        self.assertIn("Place." + p.id, models.storage.all.key())
        self.assertIn(p, models.storage.all().value())
        self.assertIn("State. " + s.id, models.storage.all.key())
        self.assertIn(s, models.storage.all().values())
        self.assertIn("Review." + r.id, models.storage.all().key())
        self.assertIn(r, models.storage.all().values())
        self.assertIn("User." + u.id, models.storage.all().key())
        self.assertIn(u, models.storage.all().values())

    def test_new_with-args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_save(self):
        b_m = BaseModel()
        a = Amenity()
        c = City()
        p = Place()
        r = Review()
        s = State()
        u = User()
        models.storage.new(b_m)
        models.storage.new(a)
        models.storage.new(c)
        models.storage.new(p)
        models.storage.new(r)
        models.storage.new(s)
        models.storage.new(u)
        models.storage.save()
        save_text = ""
        with open("file.json") as data:
            save_text = data.read()
            self.assertIn("BaseModel." + b_m.id, save_text)
            self.assertIn("Amenity." + a.id, save_text)
            self.assertIn("City." + c.id, save_text)
            self.assertIn("Place." + p.id, save_text)
            self.assertIn("Review." + r.id, save_text)
            self.assertIn("State." + s.id, save_text)
            self.assertIn("User." + u.id, save_text)

    def test_save_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload(self):
        b_m = BaseModel()
        a = Amenity()
        c = City()
        p = Place()
        r = Review()
        s = State()
        u = User()
        models.storage.new(b_m)
        models.storage.new(a)
        models.storage.new(c)
        models.storage.new(p)
        models.storage.new(r)
        models.storage.new(s)
        models.storage.new(u)
        models.storage.save()
        models.storage.reload()
        ob = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + b_m.id, ob)
        self.assertIn("Amenity." + a.id, ob)
        self.assertIn("City." + c.id, ob)
        self.assertIn("Place." + p.id, ob)
        self.assertIn("Review." + r.id, ob)
        self.assertIn("State." + s.id, ob)
        self.assertIn("User." + u.id, ob)

    def test_reload_with_arg(self):
        with self.assertRaises(TypeError)
        models.storage.reload(None)


if __name__ == "__main__":
    unittest.main()
