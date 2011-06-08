from unittest import TestCase

import html5lib_microdata

class MicrodataParserTest(TestCase):

    def test_parse(self):
        items = html5lib_microdata.get_items(open("example.html"))
        self.assertTrue(len(items), 1)

        # this html should have just one main item
        item = items[0]
        self.assertEqual(item.name, "Jane Doe")

        # properties can repeat
        self.assertEqual(item.colleagues, 
                "http://www.xyz.edu/students/alicejones.html")

        self.assertEqual(item.get_all("colleagues"), 
                ["http://www.xyz.edu/students/alicejones.html",
                 "http://www.xyz.edu/students/bobsmith.html"])

