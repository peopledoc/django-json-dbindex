# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Rodolphe Quiédeville <rodolphe@quiedeville.org>
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from django.conf import settings
from django.utils.importlib import import_module
import json
import sys
from os import path


def get_app_paths():
    """
    Return all paths defined in settings
    """
    paths = []
    for app in settings.INSTALLED_APPS:
        try:
            import_module(app)
            paths.append(sys.modules[app].__path__[0])
        except AttributeError:
            continue
    return paths

def list_indexes(fpath):
    """
    List ALL indexes
    """
    return list_indexes_drop(fpath) + list_indexes_create(fpath)

def list_indexes_create(fpath):
    """
    Read indexes
    """
    indexes = []

    pgpath = path.join(fpath, 'pgindexor_create.json')
    if path.isfile(pgpath):
        with open(pgpath) as json_data:
            indexes = json.load(json_data)
            for index in indexes:
                index['cmd'] = sql_create_from_json(index)
            json_data.close()
    return indexes

def list_indexes_drop(fpath):
    """
    Read indexes
    """
    indexes = []

    pgpath = path.join(fpath, 'pgindexor_drop.json')
    if path.isfile(pgpath):
        with open(pgpath) as json_data:
            indexes = json.load(json_data)
            for index in indexes:
                index['cmd'] = sql_drop_from_json(index)
            json_data.close()
    return indexes

def sql_create_from_json(index):
    """
    Read indexes
    """
    cmd = " ".join(["CREATE",
                    sql_unique(index),
                    "INDEX",
                    sql_concurrently(index),
                    index['name'],
                    "ON",
                    index['table'],
                    sql_using(index),
                    sql_columns(index),
                    sql_tablespace(index),
                    sql_predicat(index),
                    ";"])
    return cmd

def sql_drop_from_json(index):
    """
    Read indexes
    """
    cmd = " ".join(["DROP", index['name'], ";"])
    return cmd


def sql_unique(index):
    """
    Is the index unique or not

    return : string
    """
    res = ""
    if "unique" in index:
        if index["unique"]:
            res = "UNIQUE"
    return res

def sql_concurrently(index):
    """
    Is the index concurrently or not

    return : string
    """
    res = "CONCURRENTLY"
    if "concurrently" in index:
        if index["concurrently"] == False:
            res = ""
    return res

def sql_columns(index):
    """
    Is the index using or not

    return : string
    """
    return "(%s)" % (",".join(index['columns']))


def sql_using(index):
    """
    Is the index using or not

    return : string
    """
    return sql_simple(index, "using", "USING")

def sql_predicat(index):
    """
    Is the index predicat or not

    return : string
    """
    return sql_simple(index, "predicat", "WHERE")


def sql_tablespace(index):
    """
    create the index on a special tablespace

    return : string
    """
    return sql_simple(index, "tablespace", "TABLESPACE")


def sql_simple(index, key, prefix):
    """
    Is the index predicat or not

    return : string
    """
    res = ""
    if key in index:
        if index[key] is not None:
            res = "%s %s" % (prefix, index[key])

    return res
