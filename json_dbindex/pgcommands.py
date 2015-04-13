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
import logging
from django.db import connections


def index_exists(index, database='default'):
    """Execute raw sql
    """
    cursor = connections[database].cursor()
    qry = "SELECT COUNT(indexname) FROM pg_indexes WHERE indexname = %s"
    cursor.execute(qry, [index['name']])
    row = cursor.fetchone()
    cursor.close()
    return row[0] == 1


def execute_raw(sql, database='default', parms=None):
    """
    Execute a raw SQL command

    sql (string) : SQL command
    database (string): the database name configured in settings
    """
    try:
        cursor = connections[database].cursor()
        if parms is not None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, parms)            
        cursor.close()
        return 0
    except Exception, e:
        logging.error('Cant execute %s -- Exception raised %s' % (sql, e))
        return 1


def drop_index(index, database='default'):
    """
    Check if index exists and drop it

    index (dict) : index description
    """
    if 'database' in index:
        database = index['database']

    if index_exists(index, database):
        logging.info("Will drop %s" % index['name'])

        res = execute_raw(index['cmd'], database)

        logging.info("%s dropped" % index['name'])
    else:
        res = 1
        logging.info("%s doesn't exists" % index['name'])
    return res


def create_index(index, database='default'):
    """
    Create an index

    index (dict) : index description
       {"name": "foo",
        "database": "default",
        "cmd": "CREATE INDEX foo_idx ON table (column)"
       }
    """
    if 'database' in index:
        database = index['database']

    if index_exists(index, database):
        logging.info("%s still exists" % index['name'])
        res = 1
    else:
        logging.info("Will create %s" % index['name'])
        res = execute_raw(index['cmd'], database)
        logging.info("%s created" % index['name'])
    return res


def create_extensions(extensions, database='default'):
    """
    Create all extensions
    """
    if 'database' in index:
        database = index['database']

    for extension in extensions:
        cmd = "CREATE EXTENSION IF NOT EXISTS %s"
        logging.info("Will create extension %s on database %s" % (extension, database))
        res = execute_raw(cmd,
                          database=database,
                          parms=[extension])
        logging.info("%s created" % extension)
    return res
