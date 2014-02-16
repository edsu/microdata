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

    def test_parse_nested(self):

        # parse the html for microdata
        items = get_items(open("test-data/example-nested.html"))

        # this html should have just one main item
        self.assertTrue(len(items), 1)

        item = items[0]

        # item's type should be set
        self.assertEqual(item.itemtype, [URI("http://schema.org/Event")])

        # test case of a nested itemprop
        self.assertEqual(item.name, "Miami Heat at Philadelphia 76ers - Game 3 (Home Game 1)")

        # test case of a nested itemscope
        self.assertTrue(isinstance(item.location, Item))
        self.assertEqual(item.location.itemtype, [URI("http://schema.org/Place")])
        self.assertEqual(item.location.url, URI("wells-fargo-center.html"))

        # address should be a nested item
        self.assertTrue(isinstance(item.location.address, Item))
        self.assertEqual(item.location.address.itemtype, [URI("http://schema.org/PostalAddress")])
        self.assertTrue(item.location.address.addressLocality, "Philadelphia")

        # json
        i = json.loads(item.json())
        self.assertEqual(i["properties"]["name"][0], "Miami Heat at Philadelphia 76ers - Game 3 (Home Game 1)")
        self.assertEqual(i["type"], ["http://schema.org/Event"])
        self.assertEqual(i["properties"]["url"], ["nba-miami-philidelphia-game3.html"])
        self.assertTrue(isinstance(i["properties"]["location"][0], dict))
        self.assertEqual(i["properties"]["location"][0]["properties"]["url"][0], "wells-fargo-center.html")
        self.assertTrue(isinstance(i["properties"]["location"][0]["properties"]["address"][0], dict))
        self.assertEqual(i["properties"]["location"][0]["properties"]["address"][0]["properties"]["addressLocality"][0], "Philadelphia")
