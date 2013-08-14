import os

class Configuration(object):  
    
    if 'WERCKER_MYSQL_HOST' in os.environ:
        DATABASE = {
                'engine': 'peewee.MySQLDatabase',
                'name': os.environ['WERCKER_MYSQL_DATABASE'],
                'user': os.environ['WERCKER_MYSQL_USERNAME'],
                'host': os.environ['WERCKER_MYSQL_HOST'],
                'port': int(os.environ['WERCKER_MYSQL_PORT']),
        }
    else:
      DATABASE = {
        'name': 'spiderweb',
        'engine': 'peewee.MySQLDatabase',
        'user': 'root',
        'host': 'localhost'

      }
    DEBUG = True
