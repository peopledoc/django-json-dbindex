"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import json
from unittest import TestCase
import util

SAMPLE = """[{"name": "foo", "table": "author", "columns": ["first_name", "last_name"],
         "opcalss": null, "database": null,
         
         "predicat": null,
         "using": null,
         "tablespace": null,
         "predicat": null},
        
        {"name": "fizbuz",
         "table": "author",
         "columns": ["first_name", 
                     "last_name"],
         "opcalss": null,
         "database": null,
         
         "predicat": null,
         "using": "btree",
         "tablespace": "speedts",
         "predicat": "note IS NULL"}]
"""

class SimpleTest(TestCase):


    def test_sql_create_from_json(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        index = json.loads(SAMPLE)
        res = "CREATE INDES"
        self.assertEqual(util.sql_create_from_json(index[0]), res)
