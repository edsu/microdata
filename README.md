microdata
=========

[![Build Status](https://travis-ci.org/Rsx200/microdata-lxml.svg)](http://travis-ci.org/Rsx200/microdata-lxml)

microdata.py is a small utility library for extracting 
[HTML5 Microdata](http://dev.w3.org/html5/md/) from 
HTML. It depends on 
[html5lib](http://code.google.com/p/html5lib/)
to do the heavy lifting of building the DOM. 
For more about HTML5 Microdata check out Mark Pilgrim's 
[chapter](http://diveintohtml5.org/extensibility.html) on on it in 
[Dive Into HTML5](http://diveintohtml5.org/).

Changelog
------------
1) Added support for multiple html5lib tree builders - currently only __dom__ and __lxml__ are implemented

2) Moved parsing functions to Microdata class

3) Implemented backwards compatibility for the __get_items__ method

Command Line
------------

When you install microdata.py via pip it will be made available on the command 
line too:

    % microdata.py http://www.wdl.org/en/item/1/

This will print out the JSON for items extracted from the supplied URL.

Library
-------

Here's the basic usage from Python using https://raw.github.com/edsu/microdata/master/test-data/example.html as an example:

```python
>>> import microdata
>>> import urllib
>>> url = "https://raw.github.com/edsu/microdata/master/test-data/example.html"
>>> items = microdata.get_items(urllib.urlopen(url))
>>> item = items[0]
>>> item.itemtype
[http://schema.org/Person]
>>> item.name
u"Jane Doe"
>>> item.colleagues
u"http://www.xyz.edu/students/alicejones.html"
>>> item.get_all('colleagues')
[u"http://www.xyz.edu/students/alicejones.html", u"http://www.xyz.edu/students/bobsmith.html"]
>>> print item.json()
{
  "type": [
    "http://schema.org/Person"
  ],
  "id": "http://www.xyz.edu/~jane",
  "properties": {
    "colleagues": [
      "http://www.xyz.edu/students/alicejones.html",
      "http://www.xyz.edu/students/bobsmith.html"
    ],
    "name": [
      "Jane Doe"
    ],
    "url": [
      "http://www.janedoe.com"
    ],
    "jobTitle": [
      "Professor"
    ],
    "image": [
      "janedoe.jpg"
    ],
    "telephone": [
      "(425) 123-4567"
    ],
    "address": [
      {
        "type": [
          "http://schema.org/PostalAddress"
        ],
        "properties": {
          "addressLocality": [
            "Seattle"
          ],
          "addressRegion": [
            "WA"
          ],
          "streetAddress": [
            "\n          20341 Whitworth Institute\n          405 N. Whitworth\n        "
          ],
          "postalCode": [
            "98052"
          ]
        }
      }
    ],
    "email": [
      "mailto:jane-doe@xyz.edu"
    ]
  }
}
```

Alternative usage examples, class based:

Treebuilder: __dom__
```python
>>> from microdata import Microdata
>>> import urllib
>>> url = "https://raw.github.com/edsu/microdata/master/test-data/example.html"
>>> items = Microdata("dom").get_items(urllib.urlopen(url))
...
```

Treebuilder: __lxml__
```python
>>> from microdata import Microdata
>>> import urllib
>>> url = "https://raw.github.com/edsu/microdata/master/test-data/example.html"
>>> items = Microdata("lxml").get_items(urllib.urlopen(url))
...
```


Authors
-------

* Ed Summers <ehs@pobox.com>
* Chris Adams <chris@improbable.com>
* Razvan Muscalu <muscalu.razvan@hotmail.com>

Lincense
--------

* CC0
