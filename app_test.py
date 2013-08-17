from spider import app
from models import Connection

import os
import unittest
import demjson

class CloudTestCase(unittest.TestCase):

  def setUp(self):
    req = "{'//stackoverflow.com/questions/207510/what-is-the-key-sequence-for-closing-the-current-buffer-in-emacs': [{'timestamp': 1376718163258, 'in_node': '//www.google.com/search?q=emacs+close+buffer&rlz=1C5CHFA_enUS544US545&oq=emacs+close+bu&aqs=chrome.1.69i57j0l3.3408j0&sourceid=chrome&ie=UTF-8'}], '//www.cs.utah.edu/dept/old/texinfo/emacs18/emacs_21.html': [{'timestamp': 1376718207294, 'in_node': '//www.google.com/search?q=emacs+merge+windows&rlz=1C5CHFA_enUS544US545&oq=emacs+merge&aqs=chrome.2.69i57j0l3.4261j0&sourceid=chrome&ie=UTF-8'}], '//www.google.com/search?q=emacs+close+buffer&rlz=1C5CHFA_enUS544US545&oq=emacs+close+bu&aqs=chrome.1.69i57j0l3.3408j0&sourceid=chrome&ie=UTF-8': [{'timestamp': 1376718160856, 'in_node': ''}], '//www.google.com/search?q=emacs+merge+windows&rlz=1C5CHFA_enUS544US545&oq=emacs+merge&aqs=chrome.2.69i57j0l3.4261j0&sourceid=chrome&ie=UTF-8': [{'timestamp': 1376718205566, 'in_node': '//stackoverflow.com/questions/207510/what-is-the-key-sequence-for-closing-the-current-buffer-in-emacs'}]}" 

    def tearDown(self):
      q = Connection.delete()
      q.execute()

    def test_clouds(self):
      tester = app.test_client(self)
      response = tester.post('/', req)

      self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
  unittest.main()

