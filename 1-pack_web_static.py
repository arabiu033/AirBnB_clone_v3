#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static
folder to my AirBnB Clone repo, using the function do_pack.
"""

from datetime import datetime
from fabric.api import local
from os.path import isdir


def do_pack():
    """ Generates a .tgz archive."""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        name_of_file = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(name_of_file))
        return name_of_file
    except Exception:
        return None
