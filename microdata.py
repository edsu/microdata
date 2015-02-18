#!/usr/bin/env python

from collections import defaultdict
import sys

import html5lib

try:
    import json
except ImportError:
    import simplejson as json


class Microdata(object):
    """
    Microdata class for extracting Items from a DOM, providing a compatiblity wrapper for html5lib's trees
    """

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


    def __init__(self, tree_builder="dom"):
        """
        Define helper functions to deal with tree differences
        """
        self.tree_builder = tree_builder
        if tree_builder == "lxml":
            def attr(e, name):
                return e.get(name)

            def is_element(e):
                return True

            def text(e):
                chunks = []
                if (e.text):
                    chunks.append(e.text)
                for child in self._childNodes(e):
                    chunks.append(self._text(child))
                return ''.join(chunks)

            def childNodes(e):
                return e.getchildren()

            def tagName(e):
                return e.tag.split('}')[1]      #Strip namespaces from tag names

        else:
            def attr(e, name):
                if self._is_element(e) and e.hasAttribute(name):
                    return e.getAttribute(name)
                return None

            def is_element(e):
                return e.nodeType == e.ELEMENT_NODE

            def text(e):
                chunks = []
                if e.nodeType == e.TEXT_NODE:
                    chunks.append(e.data)
                for child in self._childNodes(e):
                    chunks.append(self._text(child))
                return ''.join(chunks)

            def childNodes(e):
                return e.childNodes

            def tagName(e):
                return e.tagName

        self._attr = attr
        self._is_element = is_element
        self._text = text
        self._childNodes = childNodes
        self._tagName = tagName


    def _find_items(self, e):
        items = []
        unlinked = []
        if self._is_element(e) and self._is_itemscope(e):
            item = self._make_item(e)
            unlinked = self._extract(e, item)
            items.append(item)
            for unlinked_element in unlinked:
                items.extend(self._find_items(unlinked_element))
        else:
            for child in self._childNodes(e):
                items.extend(self._find_items(child))

        return items


    def _extract(self, e, item):
        # looks in a DOM element for microdata to assign to an Item
        # self._extract returns a list of elements which appeared to have microdata
        # but which were not directly related to the Item that was passed in
        unlinked = []

        for child in self._childNodes(e):
            itemprop = self._attr(child, "itemprop")
            itemscope = self._is_itemscope(child)
            if itemprop and itemscope:
                nested_item = self._make_item(child)
                unlinked.extend(self._extract(child, nested_item))
                item.set(itemprop, nested_item)
            elif itemprop:
                value = self._property_value(child)
                item.set(itemprop, value)
                unlinked.extend(self._extract(child, item))
            elif itemscope:
                unlinked.append(child)
            else:
                unlinked.extend(self._extract(child, item))

        return unlinked


    def _is_itemscope(self, e):
        return self._attr(e, "itemscope") is not None


    def _property_value(self, e):
        value = None
        attrib = self.property_values.get(self._tagName(e), None)
        if attrib in ["href", "src"]:
            value = URI(self._attr(e, attrib))
        elif attrib:
            value = self._attr(e, attrib)
        else:
            value = self._text(e)
        return value


    def _make_item(self, e):
        if not self._is_itemscope(e):
            raise Exception("element is not an Item")
        itemtype = self._attr(e, "itemtype")
        itemid = self._attr(e, "itemid")
        return Item(itemtype, itemid)


    def get_items(self, location, encoding='UTF-8'):
        """
        Pass in a file or file-like object and get a list of Items present in the
        HTML document.
        """
        dom_builder = html5lib.treebuilders.getTreeBuilder(self.tree_builder)
        parser = html5lib.HTMLParser(tree=dom_builder)
        
        if (sys.version_info.major == 3):
            tree = parser.parse(location)
        else:
            tree = parser.parse(location, encoding=encoding)
        
        if (self.tree_builder == "lxml"):
            return self._find_items(tree.getroot())
        return self._find_items(tree)


class Item(object):
    """
    A class for representing a microdata Item. Item properties are accessible
    as standard Python properties, which return either a unicode string
    or another Item.
    """

    def __init__(self, itemtype=None, itemid=None):
        """Create an Item, with an optional itemptype and/or itemid.
        """
        # itemtype can be a space delimited list
        if itemtype:
            self.itemtype = [URI(i) for i in itemtype.split(" ")]

        if itemid:
            self.itemid = URI(itemid)

        self.props = {}

    def __getattr__(self, name):
        return self.get(name)

    def set(self, name, value):
        """Set an item's property
        """
        if name in self.props:
            self.props[name].append(value)
        else:
            self.props[name] = [value]

    def get(self, name):
        """Get an item's property. In cases where there are multiple values for
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


def get_items(location, encoding='UTF-8'):
    """
    Backwards compatibility
    """
    return Microdata().get_items(location, encoding)


if __name__ == "__main__":
    try:
        from urllib.request import urlopen
    except ImportError:
        from urllib import urlopen

    if len(sys.argv) < 2:
        print("Usage: %s URL [...]" % sys.argv[0])
        sys.exit(1)

    for url in sys.argv[1:]:
        sys.stderr.write(url + "\n")

        microdata = {}
        microdata['items'] = items = []

        for item in get_items(urlopen(url)):
            items.append(item.json_dict())

        print(json.dumps(microdata, indent=2))
