django-json-dbindex
===================

Describe your database index in json files into your apps

Usage
=====

Place the following two files in the root of your apps directory

* dbindex_create.json

<!-- language: json -->

[
    {"name": "july_book__foo",
     "table": "july_author",
     "columns": ["first_name", "last_name"],
     },

    {"name": "july_book__fizbuz",
     "table": "july_book",
     "columns": ["title"],
     "opclass": null,
     "database": "otherdb",     
     "predicat": null,
     "using": "gist",
     "tablespace": null,
     "predicat": "nbpages > 100"}
]


* dbindex_drop.json

The `dbindex_drop.json` is much simplier than previous, we only need to define the name of the index we will drop.

<!-- language: json -->

[
 {"name": "july_book__badindex"},
 {"name": "july_book__oldone"}
]