#!/usr/bin/python
'''
   Name:
       UITemplate

   Description:
       UITemplate builds easily parsable dictionaries from User Interface Templates
'''

from xml.dom import minidom

import shpaml
from StringUtils import interpretFromString

# Supported format types
XML = 0
SHPAML = 1

class Template(object):
    """
        A very memory efficient representation of a user interface template
    """
    __slots__ = ('create', 'accessor', 'id', 'name', 'childElements', 'properties')

    def __init__(self, create, accessor="", id="", name="", childElements=None, properties=()):
        self.create = create
        self.accessor = accessor
        self.id = id
        self.name = name
        self.childElements = childElements
        self.properties = properties

    def __getstate__(self):
        return (self.create, self.accessor, self.id, self.name, self.childElements, self.properties)

    def __setstate__(self, state):
        (self.create, self.accessor, self.id, self.name, self.childElements, self.properties) = state

    def __eq__(self, other):
        if (self.create != other.create or self.accessor != other.accessor or self.id != other.id or
            self.name != other.name or self.properties != other.properties):
            return False

        if self.childElements:
            if len(self.childElements) != len(other.childElements):
                return False
            for child, otherChild in zip(self.childElements, other.childElements):
                if not child.__eq__(otherChild):
                    return False
        elif other.childElements:
            return False

        return True

def fromFile(templateFile, formatType=SHPAML):
    """
        Returns a parsable dictionary representation of the interface:
            templateFile - a file containing an xml representation of the interface
    """
    if formatType == XML:
        return __createTemplateFromXML(minidom.parse(templateFile).childNodes[0])
    elif formatType == SHPAML:
        with open(templateFile) as openFile:
            return fromSHPAML(openFile.read())

def fromXML(xml):
    """
        Returns a parsable dictionary representation of the interface:
            xml - a string containing an xml representation of the interface
    """
    xmlStructure = minidom.parseString(xml)
    return __createTemplateFromXML(xmlStructure.childNodes[0])

def fromSHPAML(shpamlTemplate):
    """
        Returns a parsable dictionary representation of the interface:
            shpaml - a string containing a shpaml representation of the interface
    """
    xmlStructure = minidom.parseString(shpaml.convert_text(shpamlTemplate))
    return __createTemplateFromXML(xmlStructure.childNodes[0])

def __createTemplateFromXML(xml):
    """
        Parses an xml string converting it to an easily parse-able python template representation:
            xml - a string containing an xml representation of the interface
    """
    if isinstance(xml, minidom.Text):
        return xml.nodeValue.strip()

    (create, attributes, children) = (xml.tagName, xml.attributes, xml.childNodes)
    accessor = attributes.get('accessor', "")
    id = attributes.get('id', "")
    name = attributes.get('name', "")
    if accessor:
        accessor = accessor.value
        attributes.removeNamedItem('accessor')
    if id:
        id = id.value
        attributes.removeNamedItem('id')
    if name:
        name = name.value
        attributes.removeNamedItem('name')

    properties = tuple(((attribute[0], interpretFromString(attribute[1])) for attribute in attributes.items()))
    if children:
        childNodes = (__createTemplateFromXML(node) for node in children if
                      node.__class__ in (minidom.Element, minidom.Text))
        childElements = tuple(child for child in childNodes if child)
    else:
        childElements = None

    return Template(create, accessor, id, name, childElements, properties)

