"""
django-json-dbindex tests on pgcommands
"""
import os
import util
import pgcommands
from mock import MagicMock
from django.test import TestCase


class PostgreSQLTest(TestCase):

    def test_create_extensions(self):
        """
        Create a list of extensions
        """        
        pgcommands.execute_raw = MagicMock(return_value=0)
        res = pgcommands.create_extensions(['unaccent', 'pg_trgm'])
        self.assertEqual(res, 0)
