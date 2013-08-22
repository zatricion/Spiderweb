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
        q.execute()

    def test(self):
        tester = app.test_client(self)
        a_test = tester.post('/', data=dict(word='A'))
        b_test = tester.post('/', data=dict(word='B'))
        c_test = tester.post('/', data=dict(word='C'))
        d_test = tester.post('/', data=dict(word='D'))
        p_test = tester.post('/', data=dict(word='P'))
        n_test = tester.post('/', data=dict(word='N'))
        no_test = tester.post('/', data={})

        assert (a_test.data ==
           demjson.encode({"B":0.5,"C":0.1111111111111111,"D":1.1111111111111112,"Q":0.2}))

        assert (b_test.data ==
           demjson.encode({"A":0.5,"C":0.6111111111111112,"D":1.6111111111111112,"Q":0.7}))

        assert (c_test.data ==
           demjson.encode({"A":0.1111111111111111,"B":0.6111111111111112,"D":1.0,"Q":0.3111111111111111}))

        assert (d_test.data ==
           demjson.encode({"A":1.1111111111111112,"B":1.6111111111111112,"C":1.0,"Q":1.3111111111111111}))

        assert (p_test.data ==
           demjson.encode({"N":1.0,"X":1.0}))

        assert (n_test.data ==
           demjson.encode({"P":1.0,"X":2.0}))

        assert (no_test.data == "{}")

 
if __name__ == "__main__":
  unittest.main()

