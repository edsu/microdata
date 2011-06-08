microdata.py is a small utility library for extracting 
[HTML5 Microdata](http://dev.w3.org/html5/md/) from 
HTML. It depends on html5lib to do the heavy lifting of building the DOM. 
For more about HTML5 Microdata check out Mark Pilgrim's 
[chapter](http://diveintohtml5.org/extensibility.html) on on it in 
[Dive Into HTML5](http://diveintohtml5.org/).

Here's the basic usage:

```python
>>> import microdata
>>> items = microdata.parse("example.html")
>>> item = items[0]
>>> item.itemtype
u"http://schema.org/Person"
>>> item.name
u"Jane Doe"
>>> item.colleagues
u"http://www.xyz.edu/students/alicejones.html"
>>> item.get_all('colleagues')
[u"http://www.xyz.edu/students/alicejones.html", u"http://www.xyz.edu/students/bobsmith.html"]
```

Author: Ed Summers <ehs@pobox.com>
License: Public Domain
