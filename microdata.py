#!/usr/bin/env python

from collections import defaultdict
import sys

import html5lib

try:
    import json
except ImportError:
    import simplejson as json


def get_items(location, encoding='UTF-8'):
    """
    Pass in a file or file-like object and get a list of Items present in the
    HTML document.
    """
    dom_builder = html5lib.treebuilders.getTreeBuilder("dom")
    parser = html5lib.HTMLParser(tree=dom_builder)
    
    if (sys.version_info.major == 3):
        tree = parser.parse(location)
    else:
        tree = parser.parse(location, encoding=encoding)
    
    return _find_items(tree)


class Item(object):
    """
    A class for representing a microdata Item. Item properties are accessible
    as standard Python properties, which return either a unicode string
    or another Item.
    """

    def __init__(self, itemtype=None, itemid=None):
        """Create an Item, by optionally passing in an itemtype URL
        """

        # itemtype is split into a list on spaces: see
        # http://www.whatwg.org/specs/web-apps/current-work/multipage/microdata.html#attr-itemtype
        self.itemtype = []

        if itemtype:
            if isinstance(itemtype, basestring):
                types = itemtype.split(" ")
            else:
                types = itemtype
            self.itemtype = [URI(i) for i in types]

        if itemid:
            self.itemid = URI(itemid)
        self.props = {}

    def __getattr__(self, name):
        return self.get(name)

    def set(self, name, value):
        """Set an item property
        """
        if name in self.props:
            self.props[name].append(value)
        else:
            self.props[name] = [value]

    def get(self, name):
        """Get an item property. In cases where there are multiple values for
        a given property this returns only the first. If the property is
        not set None is returned.
        """
        values = self.get_all(name)
        if len(values) > 0:
            return values[0]
        return None

    def get_all(self, name):
        """Get all the values for a given property. If the property is not
        set for the Item an empty list is returned.
        """
        if name in self.props:
            return self.props[name]
        else:
            return []

    def json(self):
        """Returns the Item expressed as JSON. If there's a better JSON
        representation please let me know :-)
        """
        return json.dumps(self.json_dict(), indent=2)

    def json_dict(self):
        """Returns the item, and its nested items as a python dictionary.
        """

        item = {}

        if self.itemtype:
            item['type'] = [i.string for i in self.itemtype]
        if self.itemid:
            item['id'] = self.itemid.string

        item['properties'] = props = defaultdict(list)

        for name, values in self.props.items():
            for v in values:
                if isinstance(v, Item):
                    props[name].append(v.json_dict())
                elif isinstance(v, URI):
                    props[name].append(v.string)
                else:
                    props[name].append(v)

        return item


class URI(object):

    def __init__(self, string):
        self.string = string

    def __eq__(self, other):
        if isinstance(other, URI):
            return self.string == other.string
        return False

    def __repr__(self):
        return self.string


# what follows are the guts of extracting the Items from a DOM

property_values = {
    'meta':     'content',
    'audio':    'src',
    'embed':    'src',
    'iframe':   'src',
    'img':      'src',
    'source':   'src',
    'video':    'src',
    'a':        'href',
    'area':     'href',
    'link':     'href',
    'object':   'data',
    'time':     'datetime',
}


def _find_items(e):
    items = []
    if _is_element(e) and e.hasAttribute("itemscope"):
        item = _get_item(e)
        if item:
            items.append(item)
    else:
        for child in e.childNodes:
            items.extend(_find_items(child))
    return items


def _get_item(e, item=None):
    if not item:
        item = Item(_attr(e, "itemtype"), _attr(e, "itemid"))

    for child in e.childNodes:
        prop_name = _attr(child, "itemprop")
        if prop_name and _is_itemscope(child):
            value = _get_item(child)
            item.set(prop_name, value)
        elif prop_name:
            value = _property_value(child)
            item.set(prop_name, value)
        else:
            _get_item(child, item)

    return item

# helper functions around python's minidom


def _attr(e, name):
    if _is_element(e) and e.hasAttribute(name):
        return e.getAttribute(name)
    return None


def _is_element(e):
    return e.nodeType == e.ELEMENT_NODE


def _is_itemscope(e):
    return _attr(e, "itemscope") is not None


def _property_value(e):
    value = None
    attrib = property_values.get(e.tagName, None)
    if attrib in ["href", "src"]:
        value = URI(e.getAttribute(attrib))
    elif attrib:
        value = e.getAttribute(attrib)
    else:
        value = _text(e)
    return value


def _text(e):
    chunks = []
    if e.nodeType == e.TEXT_NODE:
        chunks.append(e.data)
    for child in e.childNodes:
        chunks.append(_text(child))
    return ''.join(chunks)

if __name__ == "__main__":
    import urllib
    if len(sys.argv) < 2:
        print "Usage: %s URL [...]" % sys.argv[0]
        sys.exit(1)

    for url in sys.argv[1:]:
        sys.stderr.write(url + "\n")

        microdata = {}
        microdata['items'] = items = []

        for item in get_items(urllib.urlopen(url)):
            items.append(item.json_dict())

        print json.dumps(microdata, indent=2)
