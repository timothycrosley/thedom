'''
    JsonParser.py

    Creates a Node tree from a python data structure (presumably originating from a JSON string)

    Copyright (C) 2015  Timothy Edmund Crosley

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

from .Base import Node, TextNode
from .Layout import Flow
from .MultiplePythonSupport import *

TYPE_MAP = {str:'string', unicode:'string', int:'integer'}

class __Tag__(Node):
    def _create(self, tagName, parent, id=None, name=None):
        Node._create(self, id, name, parent, **kwargs)
        self._tagName = tagName

def parse(data, formatted=False):
    """
        Takes a jsonable python data structure and turns it into valid xml
    """
    tree = __parse__(data, Flow())
    tree[0].attributes['xmlns:xsi'] = "http://www.w3.org/2001/XMLSchema-instance"
    tree[0].attributes['xmlns:xsd'] = "http://www.w3.org/2001/XMLSchema"
    return tree.toHTML(formatted=formatted)

def __parse__(data, parentElement):
    for key, value in iteritems(data):
        newElement = parentElement.add(__Tag__(key, parentElement))
        if type(value) == dict:
            __parse__(value, newElement)
        elif type(value) in (list, tuple):
            for item in value:
                newElement.add(__Tag__(TYPE_MAP[type(item)], newElement)).add(TextNode(item))
        elif value is None:
            newElement.tagSelfCloses = newElement.attributes['xsi:nil'] = True
        else:
            newElement.add(TextNode(value))
    return parentElement
