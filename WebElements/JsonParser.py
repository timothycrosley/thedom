'''
    Name:
        JsonParser.py

    Description:
        Creates a WebElement tree from a python data structure

'''

from Base import WebElement, TextNode
from Layout import Flow

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
    return tree.toHtml(formatted=True)

def __parse__(data, parentElement):
    for key, value in data.iteritems():
        newElement = parentElement.addChildElement(__Tag__(key, parentElement))
        if type(value) == dict:
            __parse__(value, newElement)
        elif type(value) in (list, tuple):
            for item in value:
                newElement.addChildElement(__Tag__(TYPE_MAP[type(item)], newElement)).addChildElement(TextNode(item))
        elif value == None:
            newElement.tagSelfCloses = newElement.attributes['xsi:nil'] = True
        else:
            newElement.addChildElement(TextNode(value))
    return parentElement
