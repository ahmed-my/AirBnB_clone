#!/usr/bin/python3
""" Representation of the console """
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


def parse(arg):
    brackets = re.search(r"\[(.*?)\]", arg)
    curly_braces = re.search(r"\{(.*?)\}", arg)
    if brackets is None:
        if curly_braces is None:
            return [i.strip(",") for i in split(arg)]
        else:
            symbol = split(arg[:curly_braces.span()[0]])
            result = [i.strip(",") for i in symbol]
            result.append(curly_braces.group())
            return result
    else:
        symbol = split(arg[:brackets.span()[0]])
        result = [i.strip(",") for i in symbol]
        result.apppend(brackets.group())
        return result


class HBNBCommand(cmd.Cmd):
    """ Representation of HolbertonBnB command interpreter"""

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "Amenity",
        "City",
        "Place",
        "Review",
        "State",
        "User"
    }

    def emptyline(self):
        """Represent an empty line and should do nothing"""
        pass

    def default(self, arg):
        """ Defines the response for cmd module when invalid input"""
        arg_dict = {
            "create": self.do_create,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "all": self.do_all,
            "update": self.do_update,
            "count": self.do_count
        }
        match = re.search(r"\.", arg)
        if match is not None:
            arg_match = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", arg_match[1])
            if match is not None:
                command = [arg_match[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in arg_dict.keys():
                    call = "{} {}".format(arg_match[0], command[1])
                    return arg_dict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id."""
        arg_match = parse(arg)
        if len(arg_match) == 0:
            print("** class name missing **")
        elif arg_match[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(arg_match[0])().id)
        storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id."""
        arg_match = parse(arg)
        obj_dict = storage.all()
        if len(arg_match) == 0:
            print("** class name missing **")
        elif arg_match[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg_match) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_match[0], arg_match[1]) not in obj_dict:
            print("** no instance found **")
        else:
            print(obj_dict["{}.{}".format(arg_match[0], arg_match[1])])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        arg_match = parse(arg)
        obj_dict = storage.all()
        if len(arg_match) == 0:
            print("** class name missing **")
        elif arg_match[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arg_match) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arg_match[0], arg_match[1]) not in obj_dict.keys():
            print("** no instance found **")
        else:
            del obj_dict["{}.{}".format(arg_match[0], arg_match[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        arg_match = parse(arg)
        if len(arg_match) > 0 and arg_match[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            new_object = []
            for i in storage.all().values():
                if len(arg_match) > 0 and arg_match[0] == i.__class__.__name__:
                    new_object.append(i.__str__())
                elif len(arg_match) == 0:
                    new_object.append(i.__str__())
            print(new_object)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        arg_match = parse(arg)
        obj_dict = storage.all()

        if len(arg_match) == 0:
            print("** class name missing **")
            return False
        if arg_match[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(arg_match) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(arg_match[0], arg_match[1]) not in obj_dict.keys():
            print("** no instance found **")
            return False
        if len(arg_match) == 2:
            print("** attribute name missing **")
            return False
        if len(arg_match) == 3:
            try:
                type(eval(arg_match[2])) != dict
            except NameError:
                print("** value missing **")
                return False
        if len(arg_match) == 4:
            o = obj_dict["{}.{}".format(arg_match[0], arg_match[1])]
            if arg_match[2] in o.__class__.__dict__.keys():
                value_type = type(o.__class__.__dict__[arg_match[2]])
                o.__dict__[arg_match[2]] = value_type(arg_match[3])
            else:
                o.__dict__[arg_match[2]] = arg_match[3]
        elif type(eval(arg_match[2])) == dict:
            o = obj_dict["{}.{}".format(arg_match[0], arg_match[1])]
            for key, value in eval(arg_match[2]).items():
                if (key in o.__class__.__dict__.keys() and
                   type(o.__class__.__dict__[key] in {str, int, float})):
                    value_type = type(o.__class__.__dict__[key])
                    o.__dict__[key] = value_type(value)
                else:
                    o.__dict__[key] = value
        storage.save()

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        arg_match = parse(arg)
        counter = 0
        for i in storage.all().values():
            if arg_match[0] == i.__class__.__name__:
                counter += 1
        print(counter)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
