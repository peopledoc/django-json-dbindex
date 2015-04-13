"""
django-json-dbindex tests
"""
import os
import json
import util
from django.test import TestCase


class SimpleTest(TestCase):

    def test_sql_simple(self):
        """
        Return of sql_simple
        """
        idx = {'foo': 'bar'}
        res = "FOOBAR bar"
        self.assertEqual(util.sql_simple(idx, 'foo', 'FOOBAR'), res)

    def test_sql_simple_nokey(self):
        """
        The looking key is absent
        """
        idx = {'key': 'bar'}
        res = util.sql_simple(idx, 'foo', 'FOOBAR')
        attend = ""
        self.assertEqual(res, attend)

    def test_sql_columns(self):
        """
        Build the column part of index
        """
        idx = {'foo': 'bar',
               'columns': ['foobar', 'id']}
        res = "(foobar,id)"
        self.assertEqual(util.sql_columns(idx), res)

    def test_sql_columns_operator(self):
        """
        Build the column part of index, with operator
        """
        idx = json.loads('{"foo": "bar", "columns": [{"foobar": "gist_trgm_ops"}]}')
        res = "(foobar gist_trgm_ops)"
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

    def test_sql_create_from_json_opclass(self):
        """
        Build the column part of index with an operator class
        """
        idx = {'name': 'compo1',
               'table': 'editors',
               'columns': [{'name': 'gist_trgm_ops'},
                           {'species': 'gist_trgm_ops'}],
               'using': 'GIST'}

        res = " ".join(["CREATE INDEX CONCURRENTLY compo1",
                        "ON editors USING GIST",
                        "(name gist_trgm_ops,species gist_trgm_ops)"])
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
                             'samples')
        res = util.list_indexes_create(fpath)
        self.assertEqual(len(res), 1)

    def test_list_index_drop(self):
        """
        List index to be droped
        """
        fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'samples')
        res = util.list_indexes_drop(fpath)
        self.assertEqual(len(res), 2)

    def test_list_indexes(self):
        """
        List all indexes
        """
        fpath = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'samples')
        res = util.list_indexes(fpath)
        self.assertEqual(len(res), 3)


    def test_list_extensions_multidb(self):
        """
        List all extensions
        """
        idx = [{'name': 'compo1',
                'table': 'editors',
                'columns': ['id', 'name'],
                'tablespace': 'ssd1',
                'extension': 'unaccent'},
               {'name': 'compo2',
                'table': 'editors',
                'columns': ['id', 'name'],
                'tablespace': 'ssd1',
                'extension': 'unaccent',
                'database': 'slave'}]

        extensions = util.list_extensions(idx)

        self.assertEqual(len(extensions), 2)
        self.assertTrue('default' in extensions.keys())
        self.assertTrue('slave' in extensions.keys())
        self.assertEqual(extensions['default'], ['unaccent'])
        self.assertEqual(extensions['slave'], ['unaccent'])


    def test_list_extensions_complex(self):
        """
        List all extensions
        """
        idx = [{'name': 'compo1',
                'table': 'editors',
                'columns': ['id', 'name'],
                'tablespace': 'ssd1',
                'extension': 'unaccent'},
               {'name': 'compo2',
                'table': 'editors',
                'columns': ['id', 'name'],
                'tablespace': 'ssd1',
                'extension': 'unaccent'},
               {'name': 'compo3',
                'table': 'editors',
                'columns': ['id', 'name'],
                'tablespace': 'ssd1',
                'extension': 'pg_trgm'},
               {'name': 'compo4',
                'table': 'editors',
                'columns': ['id', 'name'],
                'tablespace': 'ssd1'}]

        extensions = util.list_extensions(idx)

        self.assertEqual(len(extensions), 1)
        self.assertEqual(len(extensions['default']), 2)
        self.assertTrue('unaccent' in extensions['default'])
        self.assertTrue('pg_trgm' in extensions['default'])
