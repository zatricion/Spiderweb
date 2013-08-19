from spider import app
from models import Connection

import os
import unittest
import demjson

class CloudTestCase(unittest.TestCase):

    def setUp(self):
        Connection.create_table(fail_silently=True)

    def tearDown(self):
        q = Connection.delete()
        q.execute()

    def test_clouds(self):
        tester = app.test_client(self)
        
        req = demjson.encode({"//en.wikipedia.org/wiki/Thuringia":[{"in_node":"//en.wikipedia.org/wiki/Wartburg","timestamp":1376896096967}],"//en.wikipedia.org/wiki/Wartburg":[{"in_node":"//en.wikipedia.org/wiki/Frederick_II,_Margrave_of_Meissen","timestamp":1376895634637}],"//en.wikipedia.org/wiki/Frederick_II,_Margrave_of_Meissen":[{"in_node":"//en.wikipedia.org/wiki/Elisabeth_of_Meissen","timestamp":1376895632684}],"//en.wikipedia.org/wiki/Elisabeth_of_Meissen":[{"in_node":"","timestamp":1376895596200}]})

        response = tester.post('/add_mark', req)          
"
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
  unittest.main()

