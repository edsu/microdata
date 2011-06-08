from unittest import TestCase

import microdata

class MicrodataParserTest(TestCase):

    def test_parse(self):

        # parse the html for microdata
        items = microdata.get_items(open("example.html"))

        # this html should have just one main item
        self.assertTrue(len(items), 1)

        item = items[0]

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
