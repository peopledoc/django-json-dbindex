[![Documentation Status](https://readthedocs.org/projects/django-json-dbindex/badge/?version=latest)](https://readthedocs.org/projects/django-json-dbindex/?badge=latest)
[![Build Status](https://travis-ci.org/novafloss/django-json-dbindex.svg)](https://travis-ci.org/novafloss/django-json-dbindex)
[![Coverage Status](https://coveralls.io/repos/novafloss/django-json-dbindex/badge.svg)](https://coveralls.io/r/novafloss/django-json-dbindex)


===================
django-json-dbindex
===================

Describe your database indexes in json files into your apps directory.

Detailed documentation is in the "docs" directory.

Requirements
------------

You'll need the ``psycopg2`` package. You may want to install it via your system
packages, but if you're working on a default virtualenv (no-site-packages),
you'll have to install ``postgresql-server-dev-*``. Especially if you want to
test the application via tox.


Quick start
-----------

1. Add "json_dbindex" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'json_dbindex',
    )

2. Run `python manage.py list_dbjsindex` to list all defined indexes.


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

[{"name": "django_site_composite_idx",
  "table": "django_site",
  "columns": ["domain","name"],
  "predicat": "id > 1000",
  "unique": true,
  "concurrently": false,
  "using": "btree",
  "database": "default",
  "tablespace": "speedssd"}]
```

or with an operator class on PostgreSQL for example

```
[{"name": "django_site_composite_idx",
  "table": "django_site",
  "columns": [{"name": "gist_trgm_ops"],
  "using": "GIST",
  "extension": "pg_trgm"}]
```

Only fields, **name**, **table** and **columns** are mandatory.

```shell
$ python manage.py create_jsdbindex
```

The **concurrently** option is set by default to *true*, do you really
want your index to be created without this option ?

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

```shell
$ python manage.py drop_jsdbindex
```


Testing the app
---------------

You'll need to install tox (globally or, preferrably in a virtualenv).

The python package ``psycopg2`` must be available.

You may want to setup a postgresql server somewhere. Its credentials may live
in the ``/django-json-dbindex/demo/django_json_dbindex_demo/settings_local.py``

Example:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'json_dbindex',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```


You'll need to create at least one "json_dbindex" database on your server. Or
name it as you want.

Simply run "tox" to execute tests and other builds.
