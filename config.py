import os

import urlparse

class Configuration(object):  

  if os.environ.has_key('WERCKER_POSTGRESQL_HOST'):
    DATABASE = {
        'engine': 'peewee.PostgresqlDatabase',
        'name': os.environ['WERCKER_POSTGRESQL_DATABASE'],
        'user': os.environ['WERCKER_POSTGRESQL_USERNAME'],
        'password': os.environ['WERCKER_POSTGRESQL_PASSWORD'],
        'host': os.environ['WERCKER_POSTGRESQL_HOST'],
        'port': int(os.environ['WERCKER_POSTGRESQL_PORT']),
        }

  elif os.environ.has_key('HEROKU_POSTGRESQL_NAVY_URL'):
    urlparse.uses_netloc.append('postgres')
    url = urlparse.urlparse(os.environ['HEROKU_POSTGRESQL_NAVY_URL'])

    DATABASE = {
        'engine': 'peewee.PostgresqlDatabase',
        'name': url.path[1:],
        'user': url.username,
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
