# -*- coding: utf-8 -*-
#
# Copyright (c) 2014 Rodolphe Quiédeville <rodolphe@quiedeville.org>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of django-json-dbindex nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
#
from django.utils.importlib import import_module
from django.conf import settings
import json
import sys
import re
import logging
import pgcommands
from os import path

FILENAME_CREATE = 'dbindex_create.json'
FILENAME_DROP = 'dbindex_drop.json'


def command_check():
    """
    Check indexes
    """
    output = []
    for fpath in get_app_paths():
        for index in list_indexes_create(fpath):
            if 'database' in index:
                database = index['database']
            else:
                database = 'default'
            if pgcommands.index_exists(index, database):
                msg = "OK %s is present on %s in database %s"
                output.append(msg % (index['name'], index['table'], database))
            else:
                msg = "KO %s is missing (must be present) in database %s"
                output.append(msg % (index['name'], database))

        for index in list_indexes_drop(fpath):
            if pgcommands.index_exists(index):
                output.append("KO %s is present (must be dropped)"
                              % (index['name']))
            else:
                output.append("OK %s is missing" % (index['name']))
    return "\n".join(output)


def command_list():
    """
    List all indexes
    """
    output = []
    for fpath in get_app_paths():
        indexes = list_indexes(fpath)
        if len(indexes):
            output.append("-- Found %d index in %s\n" % (len(indexes), fpath))
            for index in indexes:
                output.append("%s\n" % (index['cmd']))
    return "\n".join(output)


def command_drop():
    """
    The drop command
    """
    # loop on apps
    for fpath in get_app_paths():
        # loop on indexes
        for index in list_indexes_drop(fpath):
            pgcommands.drop_index(index)


def command_create():
    """
    Create all indexes
    """
    for fpath in get_app_paths():
        for index in list_indexes_create(fpath):
            pgcommands.create_index(index)


def get_app_paths():
    """
    Return all paths defined in settings
    """
    fpaths = []
    for app in settings.INSTALLED_APPS:
        try:
            import_module(app)
            fpaths.append(sys.modules[app].__path__[0])
        except AttributeError:
            msg = "Can't load module %s"
            logging.error(msg % app)
            continue
    return fpaths


def list_indexes(fpath):
    """
    List ALL indexes
    """
    return list_indexes_drop(fpath) + list_indexes_create(fpath)


def list_indexes_create(fpath):
    """
    Read indexes

    return (array)
    """
    indexes = []

    pgpath = path.join(fpath, FILENAME_CREATE)
    logging.debug(pgpath)
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

    pgpath = path.join(fpath, FILENAME_DROP)
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
                    sql_predicat(index)
                    ])
    strc = re.sub('\s+', ' ', cmd)
    return re.sub('\s$', '', strc)


def sql_drop_from_json(index):
    """
    Read indexes
    """
    cmd = " ".join(["DROP INDEX",
                    index['name']])
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
        if index["concurrently"] is False:
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
