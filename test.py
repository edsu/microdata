try:
    import json
except ImportError:
    import simplejson as json

import unittest

from microdata import get_items, Item, URI

class MicrodataParserTest(unittest.TestCase):

    def test_parse(self):

        # parse the html for microdata
        items = get_items(open("test-data/example.html"))

        # this html should have just one main item
        self.assertTrue(len(items), 1)

        item = items[0]

        # item's type should be set
        self.assertEqual(item.itemtype, [URI("http://schema.org/Person")])

        # test simple case of a single valued property
        self.assertEqual(item.name, "Jane Doe")

        # but object properties can have multiple values ...
        
        # basic accessor returns the first value
        self.assertEqual(item.colleagues, 
                URI("http://www.xyz.edu/students/alicejones.html"))

        # and get_all, well, gets them all of course :)
        self.assertEqual(item.get_all("colleagues"), 
                [URI("http://www.xyz.edu/students/alicejones.html"),
                 URI("http://www.xyz.edu/students/bobsmith.html")])

        # address should be another item
        self.assertTrue(isinstance(item.address, Item))
        self.assertEqual(item.address.itemtype, [URI("http://schema.org/PostalAddress")])
        self.assertTrue(item.address.addressLocality, "Seattle")

        # json
        i = json.loads(item.json())
        self.assertEqual(i["properties"]["name"][0], "Jane Doe")
        self.assertEqual(i["type"], ["http://schema.org/Person"])
        self.assertEqual(i["id"], "http://www.xyz.edu/~jane")
        self.assertTrue(isinstance(i["properties"]["address"][0], dict))
        self.assertEqual(i["properties"]["address"][0]["properties"]["addressLocality"][0], "Seattle")
