import json

import html5lib


def get_items(location):
    dom_builder = html5lib.treebuilders.getTreeBuilder("dom")
    parser = html5lib.HTMLParser(tree=dom_builder)
    tree = parser.parse(location)
    return _find_items(tree)


class Item(object):
    """
    """

    def __init__(self, itemtype=None):
        self.itemtype = itemtype
        self.props = {}

    def __getattr__(self, name):
        return self.get(name)

    def set(self, name, value):
        if self.props.has_key(name):
            self.props[name].append(value)
        else:
            self.props[name] = [value]

    def get(self, name):
        values = self.get_all(name)
        if len(values) > 0:
            return values[0]
        return None

    def get_all(self, name):
        if self.props.has_key(name):
            return self.props[name]
        else:
            return []

    def json(self):
        return json.dumps({"type": self.itemtype, "properties": self.props},
                          indent=2)

    def __repr__(self):
        return self.json()


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
        item = Item(itemtype=_attr(e, "itemtype"))

    for child in e.childNodes:
        prop_name = _attr(child, "itemprop")
        if prop_name:
            value = _property_value(child)
            item.set(prop_name, value)
        else:
            _get_item(child, item)

    return item

def _is_element(e):
    return e.nodeType == e.ELEMENT_NODE

def _attr(e, name):
    if _is_element(e) and e.hasAttribute(name):
        return e.getAttribute(name)
    return None

def _property_value(e):
    value = None
    attrib = property_values.get(e.tagName, None)
    if attrib:
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

# where to look for property values if it isn't in the element text

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
