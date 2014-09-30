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
from ... import util
from ... import pgcommands


class Command(BaseCommand):
    help = 'Import datas'

    def handle(self, *args, **options):
        """
        Read the table book without TextField
        """
        paths = util.get_app_paths(settings)
        for path in paths:
            for index in util.list_indexes_create(path):
                if pgcommands.index_exists(index):
                    print "OK %s is present on %s" % (index['name'],
                                                      index['table'])
                else:
                    print "KO %s is missing" % (index['name'])

            for index in util.list_indexes_drop(path):
                if pgcommands.index_exists(index):
                    print "KO %s is present" % (index['name'])
                else:
                    print "OK %s is missing" % (index['name'])
