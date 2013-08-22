from spider import app
from models import Connection

import os
import unittest
import demjson

class CloudTestCase(unittest.TestCase):
    
    def setUp(self):
        Connection.create_table(fail_silently=True)
        a = Connection(from_url='A', to_url='B', count = 2)
        b = Connection(from_url='A', to_url='C', count = 9)
        c = Connection(from_url='C', to_url='D', count = 1)
        d = Connection(from_url='Q', to_url='A', count = 5)
        e = Connection(from_url='N', to_url='P', count = 1)
        f = Connection(from_url='P', to_url='X', count = 1)
        a.save()
        b.save()
        c.save()
        d.save()
        e.save()
        f.save()
        
    def tearDown(self):
        q = Connection.delete()
        #q.execute()

    def test(self):
        tester = app.test_client(self)
        response = tester.post('/', data=dict(word='A'))
        print response.data

if __name__ == "__main__":
  unittest.main()

