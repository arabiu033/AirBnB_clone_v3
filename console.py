#!/usr/bin/python3
""" Concole Module """
import cmd
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models import storage
from datetime import datetime


class HBNBCommand(cmd.Cmd):
    """
    contains the entry point of the command interpreter
    """
    __signal = 0
    prompt = "(hbnb) "
    __classes = { "BaseModel": BaseModel, "User": User, "Place": Place,
                  "State": State, "City": City, "Amenity": Amenity, "Review": Review }

    def do_create(self, line):
        """
         Creates a new instance of BaseModel,
        saves it (to the JSON file) and prints the id
        """
        try:
            if not line:
                raise SyntaxError()
            list = line.split(' ')

            kwargs = {}
            for i in range(1, len(list)):
                k, v = tuple(list[i].split('='))
                if v[0] == '"':
                    v = v.strip('"').replace('_', ' ')
                else:
                    try:
                        v = eval(v)
                    except (SyntaxError, NameError):
                        continue
                kwargs[k] = v
            if kwargs == {}:
                obj = HBNBCommand.__classes[list[0]]()
            else:
                kwargs["created_at"] = datetime.now()
                kwargs["updated_at"] = datetime.now()
                obj = HBNBCommand.__classes[list[0]](**kwargs)
                storage.new(obj)
            print(obj.id)
            obj.save()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, line):
        """
        Prints the string representation of an instance based
        on the class name and id. Ex: $ show BaseModel 1234-1234-1234
        """
        if len(line) == 0:
            print("** class name missing **")
            return

        key = line.split(" ", maxsplit=1)
        if len(key) < 2:
            print("** instance id missing **")
        elif key[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            all_obj = storage.all()
            try:
                obj = all_obj[".".join(key)]
                print(obj)
            except KeyError:
                print("** no instance found **")

    def do_destroy(self, line):
        """
        Deletes an instance based on the class name and id
        (save the change into the JSON file). Ex: $ destroy BaseModel 1234-1234-1234
        """
        if len(line) == 0:
            print("** class name missing **")
            return

        key = line.split(" ", maxsplit=1)
        if len(key) < 2:
            print("** instance id missing **")
        elif key[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            all_obj = storage.all()
            try:
                del all_obj[".".join(key)]
                storage.save()
            except KeyError:
                print("** no instance found **")

    def do_all(self, line):
        """
        Prints all string representation of all instances
        based or not on the class name. Ex: $ all BaseModel or $ all
        """
        if len(line) != 0 and  line not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            lis = []
            ins = []
            all_objs = storage.all()
            for key in all_objs.keys():
                if line == all_objs[key].__class__.__name__:
                    ins.append(all_objs[key].__str__())
                lis.append(all_objs[key].__str__())
            if HBNBCommand.__signal == 1:
                HBNBCommand.__signal = 0
                return len(ins)
            elif len(line) == 0:
                print(lis)
            else:
                print(ins)

    def do_update(self, line):
        """
        Updates an instance based on the class name and id by adding
        or updating attribute (save the change into the JSON file).
        Ex: $ update BaseModel 1234-1234-1234 email "aibnb@mail.com"
        """
        if len(line) == 0:
            print("** class name missing **")
            return
        key = line.split(" ")
        if key[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(key) == 1:
            print("** instance id missing **")
        else:
            all_obj = storage.all()
            try:
                obj = all_obj[".".join([key[0], key[1]])]
                if len(key) == 2:
                    print("** attribute name missing **")
                elif len(key) == 3:
                    print("** value missing **")
                else:
                    try:
                        value = int(key[3])
                    except ValueError:
                        if '"' in key[3]:
                            value = key[3][1:-1]
                        else:
                            value = key[3]
                    obj.__dict__[key[2]] = value
                    storage.new(obj)
                    obj.save()
            except KeyError:
                print("** no instance found **")

    def do_quit(self, line):
        """
        exit the program
        """
        return True

    def do_EOF(self, line):
        """
        exit the program
        """
        print()
        return True

    def help_quit(self):
        """
        Formated help output
        """
        print("Quit command to exit the program\n")

    def emptyline(self):
        """
        Do Nothing
        """
        pass

    def default(self, line):
        """
        Commands the consoles failed to interprete are handled here.
        """
        key = line.split(".")
        if len(key) == 1:
            return
        elif "{" and "}" and "update" in line:
            key = line.split(".update")
            s_key = key[1][1:-1].split('", ', maxsplit=1)
            if len(s_key) > 1:
                dictionary = dict(eval(s_key[1]))
                for k in dictionary.keys():
                    if '"' in s_key[0]:
                        id = s_key[0][1:]
                    else:
                        id = s_key[0]
                    self.do_update(" ".join([key[0], s_key[0][1:], k, str(dictionary[k])]))
            else:
                self.do_update(" ".join([key[0], s_key[0][1:]]))
        elif ".show" in line:
            key = line.split(".show")
            self.do_show(" ".join([key[0], key[1][2:-2]]))
        elif ".destroy" in line:
            key = line.split(".destroy")
            self.do_destroy(" ".join([key[0], key[1][2:-2]]))
        elif ".update" in line:
            key = line.split(".update")
            s_key = key[1][1:-1].split(", ")
            if len(s_key) == 1:
                self.do_update(" ".join([key[0], s_key[0][1:-1]]))
            elif len(s_key) == 2:
                self.do_update(" ".join([key[0], s_key[0][1:-1], s_key[1][1:-1]]))
            else:
                self.do_update(" ".join([key[0], s_key[0][1:-1], s_key[1][1:-1], s_key[2]]))
        else:
            if key[1] == "all()":
                self.do_all(key[0])
            elif key[1] == "count()":
                HBNBCommand.__signal = 1
                print(self.do_all(key[0]))

if __name__ == '__main__':
    HBNBCommand().cmdloop()
