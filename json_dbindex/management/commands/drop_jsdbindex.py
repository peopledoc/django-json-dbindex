#!/usr/bin/env python
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
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import connection
import logging
from ... import util


class Command(BaseCommand):
    """
    DROP all indexes defines in dbindex.json file in all apps
    """

    def handle(self, *args, **options):
        """
        Create all indexes
        """
        paths = util.get_app_paths(settings)
        for path in paths:
            for index in util.list_indexes_drop(path):
                if self.index_exists(index):
                    logging.info("Will drop %s" % index['name'])
                    self.drop_index(index)
                    logging.info("%s dropped" % index['name'])

    def drop_index(self, index):
        """
        Do drop
        """
        try:
            cursor = connection.cursor()
            cursor.execute(index['cmd'])
            cursor.close()
        except:
            pass

    def index_exists(self, index):
        """Execute raw sql
        """
        cursor = connection.cursor()
        qry = "SELECT count(indexname) FROM pg_indexes WHERE indexname = %s"
        cursor.execute(qry, [index['name']])
        row = cursor.fetchone()
        cursor.close()
        return row[0] == 1
