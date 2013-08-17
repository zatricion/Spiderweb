from spider import app
from models import Connection

import os
import unittest
import demjson

class CloudTestCase(unittest.TestCase):

  def setUp(self):
    req = {"//www.thedailybeast.com/articles/2013/08/18/ablenook-designers-offer-alternative-to-disaster-relief-tents-and-trailers.html":[{"in_node":"//www.thedailybeast.com/","timestamp":1376850655431}],"//www.thedailybeast.com/":[{"in_node":"//en.wikipedia.org/wiki/Stephen_Malkmus","timestamp":1376849398507},{"in_node":"//en.wikipedia.org/wiki/Citizens%27_band_radio","timestamp":1376852383941}],"//en.wikipedia.org/wiki/Stephen_Malkmus":[{"in_node":"//www.google.com/search?q=stephen+malkmus&rlz=1C5CHFA_enUS544US545&oq=stephen+malkmus&aqs=chrome.0.69i57j69i60j69i61j69i65l2j5.3540j0&sourceid=chrome&ie=UTF-8","timestamp":1376848374769}],"//www.google.com/search?q=stephen+malkmus&rlz=1C5CHFA_enUS544US545&oq=stephen+malkmus&aqs=chrome.0.69i57j69i60j69i61j69i65l2j5.3540j0&sourceid=chrome&ie=UTF-8":[{"in_node":"","timestamp":1376848368482}],"//en.wikipedia.org/wiki/Citizens%27_band_radio":[{"in_node":"//en.wikipedia.org/wiki/List_of_CB_slang#Trucks_and_other_non-police_vehicles","timestamp":1376852135001}],"//en.wikipedia.org/wiki/List_of_CB_slang#Trucks_and_other_non-police_vehicles":[{"in_node":"//www.google.com/search?q=cb+vehicles&rlz=1C5CHFA_enUS544US545&oq=cb+vehicles&aqs=chrome.0.69i57j0l3.7412j0&sourceid=chrome&ie=UTF-8","timestamp":1376852102137}],"//www.google.com/search?q=cb+vehicles&rlz=1C5CHFA_enUS544US545&oq=cb+vehicles&aqs=chrome.0.69i57j0l3.7412j0&sourceid=chrome&ie=UTF-8":[{"in_node":"//en.wikipedia.org/wiki/History_of_mobile_phones","timestamp":1376852096044}],"//en.wikipedia.org/wiki/History_of_mobile_phones":[{"in_node":"//www.google.com/search?q=phone+service+doctors+1960&rlz=1C5CHFA_enUS544US545&oq=phone+service+doctors+1960&aqs=chrome.0.69i57.9862j0&sourceid=chrome&ie=UTF-8","timestamp":1376851532291}],"//www.google.com/search?q=phone+service+doctors+1960&rlz=1C5CHFA_enUS544US545&oq=phone+service+doctors+1960&aqs=chrome.0.69i57.9862j0&sourceid=chrome&ie=UTF-8":[{"in_node":"//www.datamation.com/entdev/article.php/11070_3890736_2/How-to-Re-create-Mad-Men-Business-Technology.htm","timestamp":1376851298959}],"//www.datamation.com/entdev/article.php/11070_3890736_2/How-to-Re-create-Mad-Men-Business-Technology.htm":[{"in_node":"//www.datamation.com/entdev/article.php/3890736/How-to-Re-create-Mad-Men-Business-Technology.htm","timestamp":1376851267792}],"//www.datamation.com/entdev/article.php/3890736/How-to-Re-create-Mad-Men-Business-Technology.htm":[{"in_node":"//www.google.com/search?q=phone+service&rlz=1C5CHFA_enUS544US545&oq=phone+servic&aqs=chrome.1.69i57j0l3.3305j0&sourceid=chrome&ie=UTF-8","timestamp":1376851197080}],"//www.google.com/search?q=phone+service&rlz=1C5CHFA_enUS544US545&oq=phone+servic&aqs=chrome.1.69i57j0l3.3305j0&sourceid=chrome&ie=UTF-8":[{"in_node":"","timestamp":1376851133485}]}
    
    def tearDown(self):
      q = Connection.delete()
      q.execute()

    def test_clouds(self):
      tester = app.test_client(self)
      response = tester.post('/add_mark', req)
      print response

      self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
  unittest.main()

