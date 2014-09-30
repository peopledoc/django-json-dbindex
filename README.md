===================
django-json-dbindex
===================

Describe your database index in json files into your apps

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "json_dbindex" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'json_dbindex',
    )

2. Run `python manage.py list_jsindex` to list all defined indexes.


Management commands
-------------------

* list_jsdbindex
* create_jsdbindex
* drop_jsdbindex
* check_jsdbindex


Create indexes
--------------

Create a file in you app directory called `dbindex_create.json` with
following contents

```javascript

[{"name": "django_site_composite_idx"},
  "table": "django_site",
  "columns": ["domain","name"],
  "predicat": "WHERE id > 1000",
  "unique": yes,
  "concurrently": false,
  "using": "btree",     
  "tablespace": "speedssd"}]
```

Only fields, **name**, **table**, **columns** are mandatory.

The **concurrently** option is set by default, do you really want your
index to be created without this option ?

Trying to create an existing index will not generate an error, only a
logging at level notice will be raised.


Drop indexes
------------

Create a file in you app directory called `dbindex_drop.json` with
following contents.

```javascript
[{"name": "django_site_composite_idx"},
 {"name": "django_site_domain_idx"}]
```

Only the name is required. In the above example two indexes will be
dropped. Trying to drop a non existing index will not generate an
error, only a logging at level notice will be raised.
