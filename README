microdata.py is a small utility library for extracting HTML5 Microdata from 
HTML. It depends on html5lib to do the heavy lifting of building the DOM. 
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
