from app import app
from app import db

import os
import unittest
import json

class CloudTestCase(unittest.TestCase):

    def setUp(self):
      url1 = "hi"
      url2 = "bye"
      try:
          r = Connections.get(Connections.from == url1, Connections.to == url2)
          r.count += 1
      except Connections.DoesNotExist:
          r = Connections(from = url1, to = url2, count = 1)
      r.save()

    def tearDown(self)
        q = Connections.delete()
        q.execute()

    def test_clouds(self):
        tester = app.test_client(self)
        response = tester.get('/clouds.json', content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, json.dumps(['bye']))

if __name__ == "__main__":
    unittest.main()

