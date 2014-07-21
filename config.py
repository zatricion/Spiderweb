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

  elif os.environ.has_key('DATABASE_URL'):
    urlparse.uses_netloc.append('postgres')
    url = urlparse.urlparse(os.environ['DATABASE_URL'])

    DATABASE = {
        'engine': 'peewee.PostgresqlDatabase',
        'name': url.path[1:],
        'user': url.username,
        'password': url.password,
        'host': url.hostname,
        'port': url.port,
        }
    SOCIAL_GOOGLE  = {
        'consumer_key': '591770024554-9occc8nfeqfoqtb3nhd3jlmelf8qdub1.apps.googleusercontent.com',
        'consumer_secret': 'nfQ_idtD9zgCteFQsYh2fz9T',
      }
    SECURITY_POST_LOGIN_VIEW = '/profile'
    SECURITY_LOGIN_USER_TEMPLATE = 'login.html'
    SOCIAL_APP_URL =  'http://spiderweb.herokuapp.com'
    DEBUG = True

  else:
    DATABASE = {
        'name': 'spiderweb',
        'engine': 'peewee.PostgresqlDatabase',
        }

    SOCIAL_GOOGLE  = {
      'consumer_key': '591770024554-tptv9na71imv0rp9lmlei1n08gj1u7u6.apps.googleusercontent.com',
      'consumer_secret': 'lYb5QHBVrnoagQQ3TtTXUjkA',
      }
    SECURITY_POST_LOGIN_VIEW = '/profile'
    SECURITY_LOGIN_USER_TEMPLATE = 'login.html'
    DEBUG = True
 
