import os, sys
from django.conf import settings


DIRNAME = os.path.dirname(__file__)
settings.configure(DEBUG = True,
                   DATABASE_ENGINE = 'sqlite3',
                   DATABASE_NAME = os.path.join(DIRNAME, 'database.db'),
                   INSTALLED_APPS = ('django.contrib.auth',
                                     'django.contrib.contenttypes',
                                     'django.contrib.sessions',
                                     'django.contrib.admin',
                                     'json_dbindex',
                                     'json_dbindex.tests',))


from django.test.utils import setup_test_environment

setup_test_environment()

from django.test import DiscoverRunner()

