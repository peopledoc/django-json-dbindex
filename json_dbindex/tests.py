"""
django-json-dbindex tests
"""
import os
import util
from django.test import TestCase


class SimpleTest(TestCase):

    def test_sql_simple(self):
        """
        Return of sql_simple
        """
        idx = {'foo': 'bar'}
        res = "foobar bar"
        self.assertEqual(util.sql_simple(idx, 'foo', 'foobar'), res)

    def test_sql_columns(self):
        """
        Build the column part of index
        """
        idx = {'foo': 'bar',
               'columns': ['foobar', 'id']}
        res = "(foobar,id)"
        self.assertEqual(util.sql_columns(idx), res)

    def test_sql_using(self):
        """
        Build the column part of index
        """
        idx = {'using': 'btree'}

        res = "USING btree"
        self.assertEqual(util.sql_using(idx), res)

    def test_sql_predicat(self):
        """
        Build the column part of index
        """
        idx = {'using': 'btree',
               'predicat': 'foo > 3'}

        res = "WHERE foo > 3"
        self.assertEqual(util.sql_predicat(idx), res)

    def test_sql_tablespace(self):
        """
        Build the column part of index
        """
        idx = {'tablespace': 'ssd1'}

        res = "TABLESPACE ssd1"
        self.assertEqual(util.sql_tablespace(idx), res)

    def test_sql_unique(self):
        """
        Build the column part of index
        """
        idx = {'unique': True}

        res = "UNIQUE"
        self.assertEqual(util.sql_unique(idx), res)

    def test_sql_create_from_json(self):
        """
        Build the column part of index
        """
        idx = {'name': 'compo1',
               'table': 'editors',
               'columns': ['id', 'name'],
               'tablespace': 'ssd1'}

        res = " ".join(["CREATE INDEX CONCURRENTLY compo1",
                        "ON editors (id,name)",
                        "TABLESPACE ssd1"])
        self.assertEqual(util.sql_create_from_json(idx), res)

    def test_sql_drop_from_json(self):
        """
        Build the column part of index
        """
        idx = {'name': 'compo1',
               'table': 'editors',
               'columns': ['id', 'name'],
               'tablespace': 'ssd1'}

        cmd = util.sql_drop_from_json(idx)

        res = 'DROP INDEX compo1'

        self.assertEqual(cmd, res)

    def test_sql_create_from_json_full(self):
        """
        Build the column part of index
        """
        idx = {'name': 'compo1',
               'table': 'editors',
               'unique': True,
               'columns': ['id', 'name'],
               'tablespace': 'ssd1'}

        res = " ".join(["CREATE UNIQUE INDEX CONCURRENTLY compo1",
                        "ON editors (id,name)",
                        "TABLESPACE ssd1"])
        self.assertEqual(util.sql_create_from_json(idx), res)

    def test_list_index_create(self):
        """
        List index to be created
        """
        fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '..',
                             'demo',
                             'django_json_dbindex_demo',
                             'foobar')
        print fpath
        res = util.list_indexes_create(fpath)
        self.assertEqual(len(res), 1)

    def test_list_index_drop(self):
        """
        List index to be droped
        """
        fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '..',
                             'demo',
                             'django_json_dbindex_demo',
                             'foobar')
        print fpath
        res = util.list_indexes_drop(fpath)
        self.assertEqual(len(res), 2)

    def test_list_indexes(self):
        """
        List all indexes
        """
        fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             '..',
                             'demo',
                             'django_json_dbindex_demo',
                             'foobar')
        print fpath
        res = util.list_indexes(fpath)
        self.assertEqual(len(res), 3)
