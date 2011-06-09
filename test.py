import json
import unittest

import microdata

class MicrodataParserTest(unittest.TestCase):

    def test_parse(self):

        # parse the html for microdata
        items = microdata.get_items(open("test-data/example.html"))

        # this html should have just one main item
        self.assertTrue(len(items), 1)

        item = items[0]

        # item's type should be set
        self.assertEqual(item.itemtype, "http://schema.org/Person")

        # test simple case of a single valued property
        self.assertEqual(item.name, "Jane Doe")

        # but object properties can have multiple values ...
        
        # basic accessor returns the first value
        self.assertEqual(item.colleagues, 
                "http://www.xyz.edu/students/alicejones.html")

        # and get_all, well, gets them all of course :)
        self.assertEqual(item.get_all("colleagues"), 
                ["http://www.xyz.edu/students/alicejones.html",
                 "http://www.xyz.edu/students/bobsmith.html"])

        # address should be another item
        self.assertTrue(isinstance(item.address, microdata.Item))
        self.assertTrue(item.address.itemtype, "http://schema.org/PostalAddress")
        self.assertTrue(item.address.addressLocality, "Seattle")

        # json
        i = json.loads(item.json())
        self.assertEqual(i["name"][0], "Jane Doe")
        self.assertEqual(i["$itemtype"], "http://schema.org/Person")
        self.assertEqual(i["$itemid"], "http://xyz.edu/~jane")
        self.assertTrue(isinstance(i["address"][0], dict))
        self.assertEqual(i["address"][0]["addressLocality"][0], "Seattle")
