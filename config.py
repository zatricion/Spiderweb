import os

import urlparse

class Configuration(object):  

  if 'WERCKER_POSTGRESQL_HOST' in os.environ:
    DATABASE = {
        'engine': 'peewee.PostgresqlDatabase',
        'name': os.environ['WERCKER_POSTGRESQL_DATABASE'],
        'user': os.environ['WERCKER_POSTGRESQL_USERNAME'],
        'password': os.environ['WERCKER_POSTGRESQL_PASSWORD'],
        'host': os.environ['WERCKER_POSTGRESQL_HOST'],
        'port': int(os.environ['WERCKER_POSTGRESQL_PORT']),
        }

  elif 'DATABASE_URL' in os.environ:
    urlparse.uses_netloc.append('postgres')
    url = urlparse.urlparse(os.environ['DATABASE_URL'])

    DATABASE = {
        'engine': 'peewee.PostgresqlDatabase',
        'name': url.path[1:],
        'password': url.password,
        'host': url.hostname,
        'port': url.port,
        }

  else:
    DATABASE = {
        'name': 'spiderweb',
        'engine': 'peewee.MySQLDatabase',
        'user': 'root',
        'host': 'localhost'

        }
  DEBUG = True
