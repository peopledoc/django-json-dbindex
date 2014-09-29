"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import util
from django.test import TestCase


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

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
        idx = {'using': 'bar'},

        res = "using bar"
        self.assertEqual(util.sql_using(idx), res)
