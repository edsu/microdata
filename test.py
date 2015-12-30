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

        # <script> tag should be ignored in the content text
        self.assertFalse("Unrelated text" in item.address.streetAddress)

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
        self.assertEqual(item.name.strip(), "Miami Heat at Philadelphia 76ers - Game 3 (Home Game 1)")

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
        self.assertEqual(i["properties"]["name"][0].strip(), "Miami Heat at Philadelphia 76ers - Game 3 (Home Game 1)")
        self.assertEqual(i["type"], ["http://schema.org/Event"])
        self.assertEqual(i["properties"]["url"], ["nba-miami-philidelphia-game3.html"])
        self.assertTrue(isinstance(i["properties"]["location"][0], dict))
        self.assertEqual(i["properties"]["location"][0]["properties"]["url"][0], "wells-fargo-center.html")
        self.assertTrue(isinstance(i["properties"]["location"][0]["properties"]["address"][0], dict))
        self.assertEqual(i["properties"]["location"][0]["properties"]["address"][0]["properties"]["addressLocality"][0], "Philadelphia")

    def test_parse_unlinked(self):
        items = get_items(open("test-data/unlinked.html"))
        self.assertEqual(len(items), 2)

        i = items[0]
        self.assertEqual(i.itemtype, [URI("http://schema.org/Person")])
        self.assertEqual(i.name, "Jane Doe")
        self.assertEqual(i.streetAddress, None)

        # this PostalAddress is enclosed within the Person but it is 
        # not linked via the streetAddress itemprop. This particular example 
        # would represent a bug in the markup, but technically items can appear 
        # within other items without them being related together with an 
        # itemprop.

        i = items[1]
        self.assertEqual(i.itemtype, [URI("http://schema.org/PostalAddress")])
        self.assertTrue('Whitworth' in i.streetAddress)

    def test_skip_level(self):
        items = get_items(open("test-data/skip-level.html"))
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].name, "Jane Doe")

        

if __name__ == "__main__":
    unittest.main()
