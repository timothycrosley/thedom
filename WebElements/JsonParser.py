'''
    JsonParser.py

    Creates a WebElement tree from a python data structure (presumably originating from a JSON string)

    Copyright (C) 2013  Timothy Edmund Crosley

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

from .Base import WebElement, TextNode
from .Layout import Flow
from .MultiplePythonSupport import *

TYPE_MAP = {str:'string', unicode:'string', int:'integer'}

class __Tag__(WebElement):
    def _create(self, tagName, parent, id=None, name=None):
        WebElement._create(self, id, name, parent, **kwargs)
        self._tagName = tagName

def parse(data):
    """
        Takes a jsonable python data structure and turns it into valid xml
    """
    tree = __parse__(data, Flow())
    tree[0].attributes['xmlns:xsi'] = "http://www.w3.org/2001/XMLSchema-instance"
    tree[0].attributes['xmlns:xsd'] = "http://www.w3.org/2001/XMLSchema"
    return tree.toHTML(formatted=True)

def __parse__(data, parentElement):
    for key, value in iteritems(data):
        newElement = parentElement.addChildElement(__Tag__(key, parentElement))
        if type(value) == dict:
            __parse__(value, newElement)
        elif type(value) in (list, tuple):
            for item in value:
                newElement.addChildElement(__Tag__(TYPE_MAP[type(item)], newElement)).addChildElement(TextNode(item))
        elif value is None:
            newElement.tagSelfCloses = newElement.attributes['xsi:nil'] = True
        else:
            newElement.addChildElement(TextNode(value))
    return parentElement
