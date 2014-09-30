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
from django.db import connection


def index_exists(index):
    """Execute raw sql
    """
    cursor = connection.cursor()
    qry = "SELECT COUNT(indexname) FROM pg_indexes WHERE indexname = %s"
    cursor.execute(qry, [index['name']])
    row = cursor.fetchone()
    cursor.close()
    return row[0] == 1


def execute_raw(sql):
    """
    Execute a raw SQL command

    sql (string) : SQL command
    """
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        cursor.close()
        return 0
    except:
        logging.error('Cant execute %s' % sql)
        return 1


def drop_index(index):
    """
    Check if index exists and drop it

    index (dict) : index description
    """
    if index_exists(index):
        logging.info("Will drop %s" % index['name'])
        res = execute_raw(index['cmd'])
        logging.info("%s dropped" % index['name'])
    else:
        logging.notice("%s doesn't exists" % index['name'])
    return res


def create_index(index):
    """
    Create an index

    index (dict) : index description
    """
    if index_exists(index):
        logging.notice("%s still exists" % index['name'])
    else:
        logging.info("Will create %s" % index['name'])
        res = execute_raw(index['cmd'])
        logging.info("%s created" % index['name'])
    return res
