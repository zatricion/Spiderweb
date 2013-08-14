from app import app
from models import Connection

import os
import unittest
import json

class CloudTestCase(unittest.TestCase):

    def setUp(self):
      url1 = "hi"
      url2 = "bye"

      Connection.create_table(True)
      try:
          r = Connection.get(Connection.from_url == url1, Connection.to_url == url2)
          r.count += 1
      except Connection.DoesNotExist:
          r = Connection(from_url = url1, to_url = url2, count = 1)
      r.save()

    def tearDown(self):
        q = Connection.delete()
        q.execute()

    def test_clouds(self):
        tester = app.test_client(self)
        response = tester.get('/clouds.json', content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, json.dumps(['bye']))

if __name__ == "__main__":
    unittest.main()

